import unittest
from unittest.mock import MagicMock, patch

import polars
from selenium.common import WebDriverException

from src import config
from src.scraper import SubredditScraper


class TestSubredditScraper(unittest.TestCase):
    """
    Unit Test class for the SubredditScraper class.

    Attributes:
        driver_options: A MagicMock object representing options for the webdriver.
        db_client: A MagicMock object representing a database client.
        subreddit_scraper: A SubredditScraper object to perform unit tests on.

    Methods:
        setUpClass: Set up test class with common test objects.
        test_scrape_subreddit: Test the scrape_subreddit method of the SubredditScraper class.
        test_extract_post_data: Test the extract_post_data method of the SubredditScraper class.
        test_process_post: Test the process_post method of the SubredditScraper class.
        test_process_post_with_exception: Test the process_post method of the SubredditScraper class when an exception is raised.
        test_extract_author: Test the extract_author method of the SubredditScraper class.
        test_get_subreddit_url: Test the get_subreddit_url method of the SubredditScraper class.
    """
    @classmethod
    def setUpClass(cls):
        cls.driver_options = MagicMock()
        cls.db_client = MagicMock()
        cls.subreddit_scraper = SubredditScraper(cls.driver_options, cls.db_client)

    @patch("src.scraper.get_driver")
    @patch("src.scraper.handle_cookie_banner")
    @patch("src.scraper.scroll_to_bottom")
    @patch("src.scraper.WebDriverWait")
    def test_scrape_subreddit(self, mock_wait, mock_scroll, mock_handle_cookie, mock_get_driver):
        subreddit_id = 'test_subreddit'
        max_posts = 10

        driver_mock = MagicMock()
        mock_get_driver.return_value.__enter__.return_value = driver_mock
        self.subreddit_scraper.extract_post_data = MagicMock()

        self.subreddit_scraper.scrape_subreddit(subreddit_id, max_posts)

        mock_get_driver.assert_called_once_with(self.driver_options)
        driver_mock.get.assert_called_once_with(self.subreddit_scraper.get_subreddit_url(subreddit_id))
        mock_handle_cookie.assert_called_once_with(driver_mock)
        mock_scroll.assert_called_once_with(driver_mock, config.SCROLL_TIME)
        self.subreddit_scraper.extract_post_data.assert_called_once_with(driver_mock, subreddit_id, max_posts)

    @patch("src.scraper.WebDriverWait")
    def test_extract_post_data(self, mock_wait):
        driver_mock = MagicMock()
        subreddit_id = 'test_subreddit'
        max_posts = 10
        post_elements = [MagicMock(), MagicMock()]
        driver_mock.find_elements.return_value = post_elements
        self.subreddit_scraper.process_post = MagicMock()

        self.subreddit_scraper.extract_post_data(driver_mock, subreddit_id, max_posts)

        driver_mock.find_elements.assert_called_once()
        self.subreddit_scraper.process_post.assert_called()

    @patch('src.scraper.config')
    @patch('src.scraper.pl')
    @patch('src.scraper.WebDriverWait')
    def test_process_post(self, mock_wait, mock_pl, mock_config):
        mock_scraper = MagicMock()
        mock_scraper.extract_author.return_value = "author"

        test_df = polars.DataFrame(
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

        mock_scraper.extract_comments_data.return_value = test_df

        driver_mock = MagicMock()

        mock_db_client = MagicMock()
        mock_db_client.__enter__.return_value = mock_db_client
        mock_scraper.db_client = mock_db_client

        mock_logger = MagicMock()
        mock_scraper.logger = mock_logger

        href = 'https://www.reddit.com/r/test_subreddit/comments/post_id/title'

        SubredditScraper.process_post(mock_scraper, driver_mock, href)

        driver_mock.get.assert_called_once_with(href)
        mock_scraper.extract_author.assert_called_once_with(driver_mock)
        mock_scraper.extract_comments_data.assert_called_once_with(driver_mock, 'post_id')
        mock_db_client.insert_many_data.assert_any_call(mock_config.COMMENTS_COLLECTION, test_df.to_dicts())

    def test_process_post_with_exception(self):
        mock_scraper = MagicMock()
        driver_mock = MagicMock()
        driver_mock.get.side_effect = WebDriverException

        href = 'https://www.reddit.com/r/test_subreddit/comments/post_id/title'

        SubredditScraper.process_post(mock_scraper, driver_mock, href)

        driver_mock.get.assert_called_once_with(href)
        driver_mock.refresh.assert_called_once()

    @patch("src.scraper.WebDriverWait")
    def test_extract_author(self, mock_wait):
        driver_mock = MagicMock()
        author_element = MagicMock()
        author_element.text = 'test_author'
        driver_mock.find_element.return_value = author_element
        self.assertEqual(self.subreddit_scraper.extract_author(driver_mock), 'test_author')
        driver_mock.find_element.assert_called_once()

    def test_get_subreddit_url(self):
        subreddit_id = 'test_subreddit'
        expected_url = 'https://www.reddit.com/r/test_subreddit'
        self.assertEqual(self.subreddit_scraper.get_subreddit_url(subreddit_id), expected_url)


if __name__ == '__main__':
    unittest.main()
