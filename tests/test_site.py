import unittest
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from src.utils import get_driver, scroll_to_bottom
from tests.test_constants import TEST_SUBREDDIT_ID, TEST_SCROLL_TIME


class TestSiteElements(unittest.TestCase):
    """
    Unit Test class for Site Elements.

    Methods:
        setUp: Set up test environment by creating a Selenium webdriver and navigating to a test subreddit.
        tearDown: Close the Selenium webdriver after the test.
        test_posts_container_presence: Test for the presence of a posts container on the subreddit page.
        test_post_body_link_presence: Test for the presence of a post body link in the posts container.
        test_comment_presence: Test for the presence of comments on a post page.
        test_author_name_presence: Test for the presence of the author's name on a post page.
        test_cookie_banner_presence: Test for the presence of a cookie banner on the subreddit page.
    """
    def setUp(self):
        self.driver = get_driver(driver_options=Options())
        self.driver.get(f'https://www.reddit.com/r/{TEST_SUBREDDIT_ID}')

    def tearDown(self):
        self.driver.quit()

    def test_posts_container_presence(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@data-testid='post-container']")))
        except Exception as e:
            self.fail(f"Test failed due to exception: {str(e)}")

    def test_post_body_link_presence(self):
        try:
            scroll_to_bottom(self.driver, TEST_SCROLL_TIME)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@data-testid='post-container']//a[@data-click-id='body']")))
        except Exception as e:
            self.fail(f"Test failed due to exception: {str(e)}")

    def test_comment_presence(self):
        try:
            scroll_to_bottom(self.driver, TEST_SCROLL_TIME)
            post_elements = self.driver.find_elements(By.XPATH,
                                                      "//div[@data-testid='post-container']//a[@data-click-id='body']")
            if post_elements:
                post_href = post_elements[0].get_attribute('href')
                self.driver.get(post_href)
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "shreddit-comment")))
            else:
                self.fail("No post was found to check for comments")
        except Exception as e:
            self.fail(f"Test failed due to exception: {str(e)}")

    def test_author_name_presence(self):
        try:
            scroll_to_bottom(self.driver, TEST_SCROLL_TIME)
            post_elements = self.driver.find_elements(By.XPATH,
                                                      "//div[@data-testid='post-container']//a[@data-click-id='body']")
            if post_elements:
                post_href = post_elements[0].get_attribute('href')
                self.driver.get(post_href)
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'author-name')]")))
            else:
                self.fail("No post was found to check for author name")
        except Exception as e:
            self.fail(f"Test failed due to exception: {str(e)}")

    def test_cookie_banner_presence(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//span[contains(., 'cookies') or contains(., 'Technologien')]")))
        except Exception as e:
            self.fail(f"Test failed due to exception: {str(e)}")


if __name__ == '__main__':
    unittest.main()
