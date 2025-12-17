"""Tests for Pydantic models."""

import math
import os
import sys
import unittest
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from models import (
    HealthResponse,
    Job,
    SearchRequest,
    clean_date,
    clean_value,
    is_nan,
)


class TestIsNan(unittest.TestCase):
    """Tests for is_nan helper function."""

    def test_is_nan_with_none(self):
        """Test is_nan returns True for None."""
        self.assertTrue(is_nan(None))

    def test_is_nan_with_float_nan(self):
        """Test is_nan returns True for float NaN."""
        self.assertTrue(is_nan(float("nan")))

    def test_is_nan_with_math_nan(self):
        """Test is_nan returns True for math.nan."""
        self.assertTrue(is_nan(math.nan))

    def test_is_nan_with_string_nan(self):
        """Test is_nan returns True for string 'nan'."""
        self.assertTrue(is_nan("nan"))
        self.assertTrue(is_nan("NaN"))
        self.assertTrue(is_nan("NAN"))

    def test_is_nan_with_valid_string(self):
        """Test is_nan returns False for valid string."""
        self.assertFalse(is_nan("hello"))
        self.assertFalse(is_nan(""))

    def test_is_nan_with_valid_number(self):
        """Test is_nan returns False for valid numbers."""
        self.assertFalse(is_nan(0))
        self.assertFalse(is_nan(42))
        self.assertFalse(is_nan(3.14))


class TestCleanValue(unittest.TestCase):
    """Tests for clean_value helper function."""

    def test_clean_value_with_none(self):
        """Test clean_value returns None for None input."""
        self.assertIsNone(clean_value(None))

    def test_clean_value_with_nan(self):
        """Test clean_value returns None for NaN input."""
        self.assertIsNone(clean_value(float("nan")))

    def test_clean_value_with_string(self):
        """Test clean_value returns string for valid input."""
        self.assertEqual(clean_value("hello"), "hello")

    def test_clean_value_with_number(self):
        """Test clean_value converts number to string."""
        self.assertEqual(clean_value(42), "42")
        self.assertEqual(clean_value(3.14), "3.14")


class TestCleanDate(unittest.TestCase):
    """Tests for clean_date helper function."""

    def test_clean_date_with_none(self):
        """Test clean_date returns None for None input."""
        self.assertIsNone(clean_date(None))

    def test_clean_date_with_nan(self):
        """Test clean_date returns None for NaN input."""
        self.assertIsNone(clean_date(float("nan")))

    def test_clean_date_with_date_object(self):
        """Test clean_date returns date object as-is."""
        d = date(2024, 1, 15)
        result = clean_date(d)
        self.assertEqual(result, d)
        self.assertIsInstance(result, date)

    def test_clean_date_with_string(self):
        """Test clean_date returns string date as string."""
        result = clean_date("2024-01-15")
        self.assertEqual(result, "2024-01-15")


class TestSearchRequest(unittest.TestCase):
    """Tests for SearchRequest model."""

    def test_search_request_required_fields(self):
        """Test SearchRequest requires role and salary."""
        request = SearchRequest(role="Engineer", salary="100k-150k")
        self.assertEqual(request.role, "Engineer")
        self.assertEqual(request.salary, "100k-150k")

    def test_search_request_defaults(self):
        """Test SearchRequest has sensible defaults."""
        request = SearchRequest(role="Engineer", salary="100k-150k")
        self.assertEqual(request.country, "AU")
        self.assertEqual(request.location, "Australia")
        self.assertEqual(request.work_type, "all")
        self.assertEqual(request.limit, 10)

    def test_search_request_custom_values(self):
        """Test SearchRequest accepts custom values."""
        request = SearchRequest(
            role="Developer",
            country="US",
            location="San Francisco",
            salary="150k-200k",
            work_type="remote",
            limit=20,
        )
        self.assertEqual(request.country, "US")
        self.assertEqual(request.location, "San Francisco")
        self.assertEqual(request.work_type, "remote")
        self.assertEqual(request.limit, 20)

    def test_search_request_limit_bounds(self):
        """Test SearchRequest limit has bounds (1-50)."""
        # Valid limits
        request = SearchRequest(role="Engineer", salary="100k-150k", limit=1)
        self.assertEqual(request.limit, 1)
        request = SearchRequest(role="Engineer", salary="100k-150k", limit=50)
        self.assertEqual(request.limit, 50)


class TestJob(unittest.TestCase):
    """Tests for Job model."""

    def test_job_required_fields(self):
        """Test Job requires id, site, title, company, job_url."""
        job = Job(
            id="test_123",
            site="TestSite",
            title="Software Engineer",
            company="Tech Corp",
            job_url="https://example.com/job/123",
        )
        self.assertEqual(job.id, "test_123")
        self.assertEqual(job.site, "TestSite")
        self.assertEqual(job.title, "Software Engineer")

    def test_job_optional_fields_default_none(self):
        """Test Job optional fields default to None."""
        job = Job(
            id="test_123",
            site="TestSite",
            title="Engineer",
            company="Corp",
            job_url="https://example.com",
        )
        self.assertIsNone(job.location)
        self.assertIsNone(job.salary_range)
        self.assertIsNone(job.description)

    def test_job_cleans_nan_values(self):
        """Test Job validator cleans NaN values."""
        job = Job(
            id="test_123",
            site="TestSite",
            title="Engineer",
            company="Corp",
            job_url="https://example.com",
            location=float("nan"),
            salary_range="nan",
        )
        self.assertIsNone(job.location)
        self.assertIsNone(job.salary_range)

    def test_job_serializes_date(self):
        """Test Job serializes date correctly."""
        job = Job(
            id="test_123",
            site="TestSite",
            title="Engineer",
            company="Corp",
            job_url="https://example.com",
            date_posted=date(2024, 1, 15),
        )
        # Convert to dict to test serialization
        job_dict = job.model_dump()
        self.assertEqual(job_dict["date_posted"], "2024-01-15")

    def test_job_handles_string_date(self):
        """Test Job handles string date."""
        job = Job(
            id="test_123",
            site="TestSite",
            title="Engineer",
            company="Corp",
            job_url="https://example.com",
            date_posted="2024-01-15",
        )
        job_dict = job.model_dump()
        self.assertEqual(job_dict["date_posted"], "2024-01-15")


class TestHealthResponse(unittest.TestCase):
    """Tests for HealthResponse model."""

    def test_health_response(self):
        """Test HealthResponse model."""
        response = HealthResponse(status="ok")
        self.assertEqual(response.status, "ok")

    def test_health_response_to_dict(self):
        """Test HealthResponse serialization."""
        response = HealthResponse(status="healthy")
        self.assertEqual(response.model_dump(), {"status": "healthy"})


if __name__ == "__main__":
    unittest.main()
