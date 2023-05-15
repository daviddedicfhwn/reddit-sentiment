import unittest
from unittest.mock import MagicMock, patch

from selenium.webdriver.remote.webdriver import WebDriver

from src.utils import get_driver, handle_cookie_banner, scroll_to_bottom, handle_google_credential


class TestUtils(unittest.TestCase):
    """
    Unit Test class for the utility functions.

    Methods:
        test_get_driver: Test the get_driver function.
        test_handle_cookie_banner: Test the handle_cookie_banner function.
        test_scroll_to_bottom: Test the scroll_to_bottom function.
        test_handle_google_credential: Test the handle_google_credential function.
    """
    def test_get_driver(self):
        with patch('src.utils.webdriver.Firefox') as mock_firefox:
            mock_firefox.return_value = MagicMock(spec=WebDriver)
            driver = get_driver(None)
            self.assertIsInstance(driver, WebDriver)
            mock_firefox.assert_called_once()

    def test_handle_cookie_banner(self):
        with patch('src.utils.webdriver.Firefox') as mock_firefox:
            mock_driver = MagicMock(spec=WebDriver)
            mock_firefox.return_value = mock_driver
            handle_cookie_banner(mock_driver)
            mock_driver.find_element.assert_called()

    def test_scroll_to_bottom(self):
        with patch('src.utils.webdriver.Firefox') as mock_firefox:
            mock_driver = MagicMock(spec=WebDriver)
            mock_firefox.return_value = mock_driver
            scroll_time = 0.1
            with patch('src.utils.time.time') as mock_time:
                mock_time.side_effect = [1, 1, 1 + scroll_time]
                scroll_to_bottom(mock_driver, scroll_time)
                mock_driver.execute_script.assert_called()

    def test_handle_google_credential(self):
        with patch('src.utils.webdriver.Firefox') as mock_firefox:
            mock_driver = MagicMock(spec=WebDriver)
            mock_firefox.return_value = mock_driver
            handle_google_credential(mock_driver)
            mock_driver.find_element.assert_called()


if __name__ == '__main__':
    unittest.main()
