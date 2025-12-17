import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from scrapers.seek import scrape_seek

class TestSeekScraper(unittest.TestCase):
    
    @patch('scrapers.seek.requests.get')
    def test_scrape_seek_success(self, mock_get):
        # Mock HTML response
        html_content = """
        <html>
            <body>
                <article data-automation="job-card">
                    <div data-automation="jobTitle"><a href="/job/12345">Senior Dev</a></div>
                    <div data-automation="jobCompany">Tech Corp</div>
                    <div data-automation="jobLocation">Sydney</div>
                </article>
                <article data-automation="job-card">
                    <div data-automation="jobTitle"><a href="/job/67890">Junior Dev</a></div>
                    <div data-automation="jobCompany">Startup Inc</div>
                    <div data-automation="jobLocation">Melbourne</div>
                </article>
            </body>
        </html>
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = html_content
        mock_get.return_value = mock_response
        
        jobs = scrape_seek("Developer", 100000, 150000)
        
        self.assertEqual(len(jobs), 2)
        self.assertEqual(jobs[0]['title'], "Senior Dev")
        self.assertEqual(jobs[0]['company'], "Tech Corp")
        self.assertEqual(jobs[0]['id'], "seek_12345")
        
    @patch('scrapers.seek.requests.get')
    def test_scrape_seek_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response
        
        jobs = scrape_seek("Developer", 100000, 150000)
        self.assertEqual(len(jobs), 0)

if __name__ == '__main__':
    unittest.main()
