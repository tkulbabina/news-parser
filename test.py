import unittest
import os
import sqlite3
from bs4 import BeautifulSoup

class TestNewsScraping(unittest.TestCase):
    def test_scrape_news(self):
        # Mock HTML content for testing
        html_content = """
        <div class="article">
            <h2>Headline 1</h2>
            <p>Summary 1</p>
        </div>
        <div class="article">
            <h2>Headline 2</h2>
            <p>Summary 2</p>
        </div>
        """

        # Mock the response object
        class MockResponse:
            text = html_content

        # Monkey patching requests.get to return mock response
        def mock_get(url):
            return MockResponse()

        from unittest.mock import patch
        with patch('requests.get', side_effect=mock_get):
            from your_script_name import scrape_news

            # Test the scrape_news function
            expected_result = [('Headline 1', 'Summary 1'), ('Headline 2', 'Summary 2')]
            self.assertEqual(scrape_news('https://example.com/news'), expected_result)

    def test_create_news_database(self):
        # Test if the database file is created
        from your_script_name import create_news_database

        news_data = [('Headline 1', 'Summary 1'), ('Headline 2', 'Summary 2')]
        create_news_database(news_data)
        self.assertTrue(os.path.exists('news_database.db'))

        # Test if the data is inserted correctly into the database
        conn = sqlite3.connect('news_database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM news")
        rows = c.fetchall()
        conn.close()
        expected_rows = [(1, 'Headline 1', 'Summary 1'), (2, 'Headline 2', 'Summary 2')]
        self.assertEqual(rows, expected_rows)

if __name__ == '__main__':
    unittest.main()
