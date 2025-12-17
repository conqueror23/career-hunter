import unittest
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils import parse_salary, filter_jobs

class TestUtils(unittest.TestCase):
    def test_parse_salary_k(self):
        min_s, max_s = parse_salary("140k-200k")
        self.assertEqual(min_s, 140000)
        self.assertEqual(max_s, 200000)

    def test_parse_salary_full(self):
        min_s, max_s = parse_salary("100000-150000")
        self.assertEqual(min_s, 100000)
        self.assertEqual(max_s, 150000)

    def test_parse_salary_mixed(self):
        min_s, max_s = parse_salary("80k-120000")
        self.assertEqual(min_s, 80000)
        self.assertEqual(max_s, 120000)
        
    def test_invalid_format(self):
        with self.assertRaises(ValueError):
            parse_salary("100k") # Missing max

    def test_filter_jobs_relevance(self):
        role = "Software Engineer"
        jobs = [
            {'title': 'Senior Software Engineer'},
            {'title': 'Junior Developer'},     # Synonym
            {'title': 'Contract Administrator'}, # Irrelevant
            {'title': 'Mechanical Designer Draftsman'}, # Irrelevant
            {'title': 'Python Engineer'},      # Relevant
            {'title': 'Chef'}                  # Irrelevant
        ]
        
        filtered = filter_jobs(jobs, role)
        titles = [j['title'] for j in filtered]
        
        self.assertIn('Senior Software Engineer', titles)
        self.assertIn('Junior Developer', titles) # Developer ~ Engineer
        self.assertIn('Python Engineer', titles)
        self.assertNotIn('Contract Administrator', titles)
        self.assertNotIn('Mechanical Designer Draftsman', titles)
        self.assertNotIn('Chef', titles)

if __name__ == '__main__':
    unittest.main()