"""Tests for utility functions."""

import os
import sys
import unittest

# Add backend/src to path properly
backend_src = os.path.join(os.path.dirname(__file__), "..", "src")
sys.path.insert(0, backend_src)

# Import using the actual config module
from utils import filter_by_work_type, filter_jobs, parse_salary


class TestParseSalary(unittest.TestCase):
    """Tests for parse_salary function."""

    def test_parse_salary_k_notation(self):
        """Test parsing salary with 'k' notation."""
        min_s, max_s = parse_salary("140k-200k")
        self.assertEqual(min_s, 140000)
        self.assertEqual(max_s, 200000)

    def test_parse_salary_full_numbers(self):
        """Test parsing salary with full numbers."""
        min_s, max_s = parse_salary("100000-150000")
        self.assertEqual(min_s, 100000)
        self.assertEqual(max_s, 150000)

    def test_parse_salary_mixed_format(self):
        """Test parsing salary with mixed format."""
        min_s, max_s = parse_salary("80k-120000")
        self.assertEqual(min_s, 80000)
        self.assertEqual(max_s, 120000)

    def test_parse_salary_with_spaces(self):
        """Test parsing salary with spaces."""
        min_s, max_s = parse_salary("100k - 200k")
        self.assertEqual(min_s, 100000)
        self.assertEqual(max_s, 200000)

    def test_parse_salary_with_commas(self):
        """Test parsing salary with commas."""
        min_s, max_s = parse_salary("100,000-200,000")
        self.assertEqual(min_s, 100000)
        self.assertEqual(max_s, 200000)

    def test_parse_salary_decimal_k(self):
        """Test parsing salary with decimal k notation."""
        min_s, max_s = parse_salary("150.5k-200k")
        self.assertEqual(min_s, 150500)
        self.assertEqual(max_s, 200000)

    def test_invalid_format_missing_max(self):
        """Test invalid format with missing max."""
        with self.assertRaises(ValueError):
            parse_salary("100k")

    def test_invalid_format_no_range(self):
        """Test invalid format with no range separator."""
        with self.assertRaises(ValueError):
            parse_salary("100000")

    def test_invalid_format_non_numeric(self):
        """Test invalid format with non-numeric value."""
        with self.assertRaises(ValueError):
            parse_salary("abc-def")


class TestFilterJobs(unittest.TestCase):
    """Tests for filter_jobs function."""

    def test_filter_jobs_exact_match(self):
        """Test filtering with exact title match."""
        jobs = [
            {"title": "Software Engineer"},
            {"title": "Data Analyst"},
        ]
        filtered = filter_jobs(jobs, "Software Engineer")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["title"], "Software Engineer")

    def test_filter_jobs_synonym_match(self):
        """Test filtering with synonym match (engineer <-> developer)."""
        jobs = [
            {"title": "Senior Software Engineer"},
            {
                "title": "Software Developer"
            },  # Has both 'software' and 'developer' (synonym of engineer)
            {"title": "Python Developer"},  # Only has 'developer', missing 'software'
            {"title": "Chef"},
        ]
        filtered = filter_jobs(jobs, "Software Engineer")
        titles = [j["title"] for j in filtered]

        # Filter requires ALL significant words to match
        self.assertIn("Senior Software Engineer", titles)
        self.assertIn("Software Developer", titles)  # software + developer (synonym of engineer)
        self.assertNotIn("Python Developer", titles)  # Missing 'software'
        self.assertNotIn("Chef", titles)

    def test_filter_jobs_manager_synonyms(self):
        """Test filtering with manager synonyms."""
        jobs = [
            {"title": "Engineering Manager"},  # Has engineering (synonym of engineer) + manager
            {"title": "Tech Lead"},  # Has 'lead' (synonym of manager), but no 'engineer'
            {
                "title": "Development Director"
            },  # Has development (synonym of developer/engineer) + director (synonym of manager)
            {"title": "Software Engineer"},  # Has 'engineer' but no 'manager'
            {"title": "Engineering Lead"},  # Has engineering + lead (synonym of manager)
        ]
        filtered = filter_jobs(jobs, "Engineer Manager")
        titles = [j["title"] for j in filtered]

        # Filter requires ALL significant words: 'engineer' AND 'manager' (with synonyms)
        self.assertIn("Engineering Manager", titles)
        self.assertIn("Development Director", titles)
        self.assertIn("Engineering Lead", titles)
        self.assertNotIn("Tech Lead", titles)  # Missing 'engineer' equivalent
        self.assertNotIn("Software Engineer", titles)  # Missing 'manager' equivalent

    def test_filter_jobs_ignores_stop_words(self):
        """Test that stop words are ignored in matching."""
        jobs = [
            {"title": "Senior Software Engineer"},
            {"title": "Junior Software Developer"},
        ]
        filtered = filter_jobs(jobs, "Senior Software Engineer")
        # Should match both because 'senior' is a stop word
        self.assertEqual(len(filtered), 2)

    def test_filter_jobs_empty_list(self):
        """Test filtering empty job list."""
        filtered = filter_jobs([], "Software Engineer")
        self.assertEqual(len(filtered), 0)

    def test_filter_jobs_na_title(self):
        """Test filtering skips N/A titles."""
        jobs = [
            {"title": "N/A"},
            {"title": "Software Engineer"},
        ]
        filtered = filter_jobs(jobs, "Software Engineer")
        self.assertEqual(len(filtered), 1)

    def test_filter_jobs_empty_title(self):
        """Test filtering skips empty titles."""
        jobs = [
            {"title": ""},
            {"title": "Software Engineer"},
        ]
        filtered = filter_jobs(jobs, "Software Engineer")
        self.assertEqual(len(filtered), 1)

    def test_filter_jobs_case_insensitive(self):
        """Test case insensitive matching."""
        jobs = [
            {"title": "SOFTWARE ENGINEER"},
            {"title": "software developer"},
        ]
        filtered = filter_jobs(jobs, "Software Engineer")
        self.assertEqual(len(filtered), 2)


class TestFilterByWorkType(unittest.TestCase):
    """Tests for filter_by_work_type function."""

    def test_filter_all_returns_all(self):
        """Test 'all' work type returns all jobs."""
        jobs = [
            {"title": "Job 1", "is_remote": True},
            {"title": "Job 2", "is_remote": False},
        ]
        filtered = filter_by_work_type(jobs, "all")
        self.assertEqual(len(filtered), 2)

    def test_filter_remote_by_is_remote_flag(self):
        """Test remote filter using is_remote flag."""
        jobs = [
            {"title": "Remote Job", "is_remote": True, "location": "Sydney"},
            {"title": "Office Job", "is_remote": False, "location": "Melbourne"},
        ]
        filtered = filter_by_work_type(jobs, "remote")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["title"], "Remote Job")

    def test_filter_remote_by_location_text(self):
        """Test remote filter using location text."""
        jobs = [
            {"title": "Remote Job", "is_remote": False, "location": "Remote, Australia"},
            {"title": "Office Job", "is_remote": False, "location": "Sydney CBD"},
        ]
        filtered = filter_by_work_type(jobs, "remote")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["title"], "Remote Job")

    def test_filter_remote_by_description(self):
        """Test remote filter using description text."""
        jobs = [
            {
                "title": "Job 1",
                "is_remote": False,
                "location": "Sydney",
                "description": "Work from home available",
            },
            {
                "title": "Job 2",
                "is_remote": False,
                "location": "Melbourne",
                "description": "In office only",
            },
        ]
        filtered = filter_by_work_type(jobs, "remote")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["title"], "Job 1")

    def test_filter_hybrid(self):
        """Test hybrid filter."""
        jobs = [
            {"title": "Hybrid Job", "location": "Sydney (Hybrid)"},
            {"title": "Remote Job", "location": "Remote"},
            {"title": "Office Job", "location": "Melbourne"},
        ]
        filtered = filter_by_work_type(jobs, "hybrid")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["title"], "Hybrid Job")

    def test_filter_onsite(self):
        """Test onsite filter excludes remote and hybrid."""
        jobs = [
            {"title": "Hybrid Job", "location": "Sydney (Hybrid)", "is_remote": False},
            {"title": "Remote Job", "location": "Remote", "is_remote": True},
            {"title": "Office Job", "location": "Melbourne CBD", "is_remote": False},
        ]
        filtered = filter_by_work_type(jobs, "onsite")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["title"], "Office Job")

    def test_filter_empty_list(self):
        """Test filtering empty job list."""
        filtered = filter_by_work_type([], "remote")
        self.assertEqual(len(filtered), 0)

    def test_filter_handles_none_values(self):
        """Test filtering handles None values gracefully."""
        jobs = [
            {"title": "Job", "is_remote": None, "location": None, "description": None},
        ]
        # Should not raise an error
        filtered = filter_by_work_type(jobs, "remote")
        self.assertEqual(len(filtered), 0)


if __name__ == "__main__":
    unittest.main()
