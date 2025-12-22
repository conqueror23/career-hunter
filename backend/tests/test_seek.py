"""Tests for Seek scraper."""

import os
import sys
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

# Add backend to path (so we can import src as a package)
backend_dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, backend_dir)

# Import using the actual config module
from src.scrapers.seek import _extract_job_id, _extract_work_type, scrape_seek


class TestSeekHelpers(unittest.TestCase):
    """Tests for Seek helper functions."""

    def test_extract_job_id_valid(self):
        """Test extracting job ID from valid URL."""
        job_id = _extract_job_id("https://www.seek.com.au/job/12345")
        self.assertEqual(job_id, "seek_12345")

    def test_extract_job_id_with_params(self):
        """Test extracting job ID from URL with parameters."""
        job_id = _extract_job_id("https://www.seek.com.au/job/67890?tracking=abc")
        self.assertEqual(job_id, "seek_67890")

    def test_extract_job_id_invalid(self):
        """Test extracting job ID from invalid URL."""
        job_id = _extract_job_id("https://www.seek.com.au/search")
        self.assertEqual(job_id, "seek_unknown")

    def test_extract_work_type_remote(self):
        """Test detecting remote work type."""
        is_remote, work_type = _extract_work_type("Sydney, Remote")
        self.assertTrue(is_remote)
        self.assertEqual(work_type, "remote")

    def test_extract_work_type_hybrid(self):
        """Test detecting hybrid work type."""
        is_remote, work_type = _extract_work_type("Melbourne (Hybrid)")
        self.assertFalse(is_remote)
        self.assertEqual(work_type, "hybrid")

    def test_extract_work_type_work_from_home(self):
        """Test detecting work from home."""
        is_remote, work_type = _extract_work_type("Work From Home, Australia")
        self.assertTrue(is_remote)
        self.assertEqual(work_type, "")  # Only "remote" keyword sets work_type

    def test_extract_work_type_onsite(self):
        """Test detecting on-site (default)."""
        is_remote, work_type = _extract_work_type("Sydney CBD")
        self.assertFalse(is_remote)
        self.assertEqual(work_type, "")

    def test_extract_work_type_none(self):
        """Test handling None location."""
        is_remote, work_type = _extract_work_type(None)
        self.assertFalse(is_remote)
        self.assertEqual(work_type, "")


class TestSeekScraperIntegration(unittest.IsolatedAsyncioTestCase):
    """Integration tests for Seek scraper - tests the scraping logic."""

    def setUp(self):
        """Set up test fixtures."""
        self.base_url = "https://www.seek.com.au/jobs"
        self.user_agent = "Mozilla/5.0 Test Agent"

    @patch("httpx.AsyncClient")
    async def test_scrape_seek_returns_jobs_from_html(self, mock_client_cls):
        """Test that scraper parses HTML correctly."""
        html_content = """
        <html>
            <body>
                <article data-automation="job-card">
                    <a data-automation="jobTitle" href="/job/12345">Senior Developer</a>
                    <span data-automation="jobCompany">Tech Corp</span>
                    <span data-automation="jobLocation">Sydney</span>
                </article>
            </body>
        </html>
        """

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = html_content

        # Setup mock client context manager
        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response
        mock_client_cls.return_value.__aenter__.return_value = mock_client

        jobs = await scrape_seek("Senior Developer", 100000, 200000)

        self.assertEqual(len(jobs), 1)
        job = jobs[0]
        self.assertEqual(job["title"], "Senior Developer")
        self.assertEqual(job["company"], "Tech Corp")
        self.assertEqual(job["id"], "seek_12345")

    @patch("httpx.AsyncClient")
    async def test_scrape_seek_handles_500_error(self, mock_client_cls):
        """Test that scraper handles server errors gracefully."""
        mock_response = MagicMock()
        mock_response.status_code = 500

        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response
        mock_client_cls.return_value.__aenter__.return_value = mock_client

        jobs = await scrape_seek("Senior Developer", 100000, 200000)
        self.assertEqual(len(jobs), 0)

    @patch("httpx.AsyncClient")
    async def test_scrape_seek_handles_empty_html(self, mock_client_cls):
        """Test that scraper handles empty HTML gracefully."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body></body></html>"

        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response
        mock_client_cls.return_value.__aenter__.return_value = mock_client

        jobs = await scrape_seek("Senior Developer", 100000, 200000)
        self.assertEqual(len(jobs), 0)


if __name__ == "__main__":
    unittest.main()
