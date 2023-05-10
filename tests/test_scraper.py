import unittest
from unittest.mock import MagicMock, patch

import polars as pl
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from src.scraper import SubredditScraper


class TestSubredditScraper(unittest.TestCase):

    @patch('src.scraper.get_driver')
    def test_scrape_subreddit(self, mock_get_driver):
        mock_driver = MagicMock(spec=WebDriver)
        mock_driver.current_url = 'https://www.reddit.com/r/test_subreddit/'

        mock_get_driver.return_value.__enter__.return_value = mock_driver

        scraper = SubredditScraper(None, None)
        scraper.extract_post_data = MagicMock()

        scraper.scrape_subreddit("test_subreddit", None)

        mock_get_driver.assert_called_once()
        scraper.extract_post_data.assert_called_once_with(mock_driver, None)

    @patch('src.database.MongoDBClient.insert_many_data')
    @patch('src.scraper.SubredditScraper.extract_comments_data')
    def test_extract_post_data(self, mock_extract_comments_data, mock_insert_many_data):
        mock_driver = MagicMock(spec=WebDriver)

        # Create the WebElement mock and set the get_attribute return value
        mock_element = MagicMock(spec=WebElement)
        mock_element.get_attribute.return_value = 'https://www.reddit.com/r/test_subreddit/comments/p1/post_title/'

        mock_driver.find_elements.return_value = [mock_element]

        scraper = SubredditScraper(None, None)

        mock_extract_comments_data.return_value = pl.DataFrame(
            {
                'post_id': ['p1'],
                'text': ['comment text'],
                'subreddit': ['test_subreddit'],
                'author': ['test_author'],
                'upvotes': [10],
                'thing_id': ['t1'],
                'parent_id': ['p1']
            }
        )

        with patch.object(WebDriverWait, 'until', return_value=True):
            scraper.extract_post_data(mock_driver)

        self.assertEqual(mock_insert_many_data.call_count, 0)
        mock_extract_comments_data.assert_called_once_with(mock_driver, 'p1')

    def test_extract_comments_data(self):
        mock_driver = MagicMock(spec=WebDriver)
        mock_comment_element = MagicMock(spec=WebElement)
        mock_driver.find_elements.return_value = [mock_comment_element]

        scraper = SubredditScraper(None, None)

        # Mock the necessary WebElement attributes and methods
        mock_comment_element.get_attribute.side_effect = lambda attr: {
            "author": "test_author",
            "thingid": "t1",
            "parentid": "p1",
            "score": "10",
            "permalink": "/r/test_subreddit/comments/.../"
        }.get(attr, "")
        mock_comment_element.find_element.return_value.text = "comment text"

        df_comments = scraper.extract_comments_data(mock_driver, "p1")

        self.assertEqual(len(df_comments), 1)
        self.assertEqual(df_comments['post_id'][0], 'p1')


if __name__ == "__main__":
    unittest.main()
