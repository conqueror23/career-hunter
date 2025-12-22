"""Integration tests for the FastAPI server."""

import os
import sys
import unittest

# Get paths and add to sys.path
tests_dir = os.path.dirname(__file__)
backend_dir = os.path.dirname(tests_dir)
src_dir = os.path.join(backend_dir, "src")
sys.path.insert(0, src_dir)
sys.path.insert(0, backend_dir)

# Clean up any MockConfig that may have polluted sys.modules from other tests
if "config" in sys.modules and hasattr(sys.modules["config"], "__class__"):
    if sys.modules["config"].__class__.__name__ == "MockConfig":
        del sys.modules["config"]

from fastapi.testclient import TestClient

# Import the server module - works both ways
try:
    import src.server as server_module
except ImportError:
    import server as server_module

app = server_module.app
search_cache = server_module.search_cache
LRUCache = server_module.LRUCache

# Import models
try:
    from src.models import SearchRequest
except ImportError:
    from models import SearchRequest


class TestHealthEndpoint(unittest.TestCase):
    """Tests for the /health endpoint."""

    def setUp(self):
        self.client = TestClient(app)

    def test_health_check_returns_ok(self):
        """Test health check returns status ok."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})


class TestSearchEndpoint(unittest.TestCase):
    """Tests for the /api/search endpoint."""

    def setUp(self):
        self.client = TestClient(app)
        # Clear cache before each test
        search_cache._cache.clear()

    def test_search_invalid_salary_format(self):
        """Test search with invalid salary format returns 400."""
        response = self.client.post(
            "/api/search",
            json={
                "role": "Software Engineer",
                "country": "AU",
                "location": "Sydney",
                "salary": "invalid",
                "work_type": "all",
                "limit": 10,
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("detail", response.json())

    def test_search_missing_required_fields(self):
        """Test search with missing required fields returns 422."""
        response = self.client.post(
            "/api/search",
            json={
                "role": "Software Engineer",
                # Missing other required fields
            },
        )
        self.assertEqual(response.status_code, 422)


class TestLRUCache(unittest.TestCase):
    """Tests for the LRU cache implementation."""

    def setUp(self):
        search_cache._cache.clear()

    def test_cache_respects_maxsize(self):
        """Test cache evicts oldest entries when full."""
        cache = LRUCache(maxsize=3, ttl=3600)

        # Add 4 items to cache with maxsize 3
        for i in range(4):
            request = SearchRequest(
                role=f"Role {i}",
                country="AU",
                location="Sydney",
                salary="100k-200k",
                work_type="all",
                limit=10,
            )
            cache.set(request, [{"id": i}])

        # Cache should only have 3 items
        self.assertEqual(len(cache._cache), 3)

        # First item should be evicted
        first_request = SearchRequest(
            role="Role 0",
            country="AU",
            location="Sydney",
            salary="100k-200k",
            work_type="all",
            limit=10,
        )
        self.assertIsNone(cache.get(first_request))

    def test_cache_key_normalization(self):
        """Test that cache normalizes keys (case insensitive)."""
        cache = LRUCache(maxsize=10, ttl=3600)

        # Add item with mixed case
        request1 = SearchRequest(
            role="Software Engineer",
            country="au",
            location="Sydney",
            salary="100k-200k",
            work_type="all",
            limit=10,
        )
        cache.set(request1, [{"id": 1}])

        # Retrieve with different case - should match due to normalization
        request2 = SearchRequest(
            role="software engineer",
            country="AU",
            location="sydney",
            salary="100k-200k",
            work_type="all",
            limit=10,
        )
        result = cache.get(request2)
        self.assertIsNotNone(result)
        self.assertEqual(result[0]["id"], 1)


if __name__ == "__main__":
    unittest.main()
