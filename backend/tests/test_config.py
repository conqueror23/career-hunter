"""Tests for configuration module."""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config import (
    CORS_ORIGINS,
    COUNTRY_MAP,
    JOB_SYNONYMS,
    STOP_WORDS,
    WORK_TYPE_KEYWORDS,
    SEEK_BASE_URL,
)


class TestConfigValues(unittest.TestCase):
    """Tests for configuration values."""

    def test_cors_origins_has_localhost(self):
        """Test CORS origins includes localhost for development."""
        self.assertIn("http://localhost:3000", CORS_ORIGINS)
        self.assertIn("http://127.0.0.1:3000", CORS_ORIGINS)

    def test_country_map_has_required_countries(self):
        """Test country map has required country codes."""
        required_countries = ["AU", "US", "UK", "NZ", "CA"]
        for country in required_countries:
            self.assertIn(country, COUNTRY_MAP)

    def test_country_map_values_are_strings(self):
        """Test country map values are lowercase strings."""
        for code, name in COUNTRY_MAP.items():
            self.assertIsInstance(name, str)
            self.assertEqual(name, name.lower())

    def test_job_synonyms_has_engineer_developer(self):
        """Test synonyms include engineer/developer relationship."""
        self.assertIn("engineer", JOB_SYNONYMS)
        self.assertIn("developer", JOB_SYNONYMS["engineer"])
        self.assertIn("developer", JOB_SYNONYMS)
        self.assertIn("engineer", JOB_SYNONYMS["developer"])

    def test_job_synonyms_has_manager_synonyms(self):
        """Test synonyms include manager related terms."""
        self.assertIn("manager", JOB_SYNONYMS)
        self.assertIn("lead", JOB_SYNONYMS["manager"])
        self.assertIn("director", JOB_SYNONYMS["manager"])

    def test_stop_words_contains_common_words(self):
        """Test stop words contains common filter words."""
        common_stop_words = ["senior", "junior", "the", "a", "and"]
        for word in common_stop_words:
            self.assertIn(word, STOP_WORDS)

    def test_work_type_keywords_has_remote(self):
        """Test work type keywords includes remote options."""
        self.assertIn("remote", WORK_TYPE_KEYWORDS)
        self.assertIn("remote", WORK_TYPE_KEYWORDS["remote"])
        self.assertIn("work from home", WORK_TYPE_KEYWORDS["remote"])

    def test_work_type_keywords_has_hybrid(self):
        """Test work type keywords includes hybrid."""
        self.assertIn("hybrid", WORK_TYPE_KEYWORDS)
        self.assertIn("hybrid", WORK_TYPE_KEYWORDS["hybrid"])

    def test_seek_base_url_is_valid(self):
        """Test Seek base URL is valid."""
        self.assertTrue(SEEK_BASE_URL.startswith("https://"))
        self.assertIn("seek.com.au", SEEK_BASE_URL)


class TestSynonymConsistency(unittest.TestCase):
    """Tests for synonym consistency."""

    def test_synonyms_are_sets(self):
        """Test all synonym values are sets."""
        for key, value in JOB_SYNONYMS.items():
            self.assertIsInstance(value, set, f"Synonym for '{key}' should be a set")

    def test_synonyms_dont_contain_themselves(self):
        """Test synonyms don't contain themselves as values."""
        for key, synonyms in JOB_SYNONYMS.items():
            self.assertNotIn(key, synonyms, f"'{key}' should not be in its own synonyms")


if __name__ == '__main__':
    unittest.main()
