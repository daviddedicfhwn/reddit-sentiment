import logging

import polars as pl
from selenium.common import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src import config
from src.utils import get_driver, handle_cookie_banner, scroll_to_bottom

# Each import should be on separate line according to PEP8
logger = logging.getLogger(__name__)


class SubredditScraper:
    def __init__(self, driver_options, db_client):
        self.driver_options = driver_options
        self.db_client = db_client

    def scrape_subreddit(self, subreddit_id, max_posts=None):
        """
        Scrapes a subreddit and saves the data to the database.
        :param subreddit_id: subreddit to scrape
        :param max_posts: maximum number of posts to scrape
        """
        try:
            with get_driver(self.driver_options) as driver:
                driver.get(self.get_subreddit_url(subreddit_id))
                WebDriverWait(driver, 10).until(EC.url_matches(r"https://www.reddit.com/r/.*"))

                handle_cookie_banner(driver)

                logger.info(f"Scrolling {config.SCROLL_TIME} seconds...")
                scroll_to_bottom(driver, config.SCROLL_TIME)
                logger.info("Scrolling finished")

                logger.info("Extracting post data...")
                self.extract_post_data(driver, subreddit_id, max_posts)
                logger.info(f"Post data extraction complete for subreddit: {subreddit_id}")

        except (TimeoutException, WebDriverException) as e:
            logger.error(f"WebDriver error during subreddit scraping: {str(e)}")
        except Exception as e:
            logger.error(f"Unknown error during subreddit scraping: {str(e)}")

    def extract_post_data(self, driver, subreddit_id, max_posts=None):
        """
        Extracts post data from the subreddit page.
        :param driver: Selenium webdriver instance.
        :param subreddit_id: Subreddit ID.
        :param max_posts: maximum number of posts to extract.
        """
        try:
            post_elements = driver.find_elements(By.XPATH,
                                                 "//div[@data-testid='post-container' and not(descendant::span[contains(text(), 'nsfw')])]//a[@data-click-id='body']")

            post_hrefs = [element.get_attribute('href') for element in post_elements]

            logger.info(f"Found {len(post_hrefs)} posts")

            if max_posts:
                logger.info(f"Limiting posts to {max_posts}")
                post_hrefs = post_hrefs[:max_posts]

            for i, href in enumerate(post_hrefs):
                self.process_post(driver, href)
                if (i + 1) % 10 == 0:
                    logger.info(f"subreddit: {subreddit_id}; processed {i + 1}/{len(post_hrefs)} posts")

        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"NoSuchElementException during post data extraction: {str(e)}")
        except Exception as e:
            logger.error(f"Unknown error during post data extraction: {str(e)}")

    def process_post(self, driver, href):
        """
        Processes a single post by extracting the post data and the comments data.
        :param driver: Selenium webdriver instance.
        :param href: link to the post.
        """
        try:
            driver.get(href)
        except (TimeoutException, WebDriverException) as e:
            logger.error(f"WebDriver error while getting href: {href}, {str(e)}. Continue with next.")
            driver.refresh()
            return
        except Exception as e:
            logger.error(f"Unknown error while getting href: {href}, {str(e)}. Continue with next.")
            driver.refresh()
            return

        split_url = href.split('/')
        post_id = split_url[6]
        subreddit = split_url[4]
        title = split_url[7]

        WebDriverWait(driver, 10).until(EC.url_contains(subreddit))

        author = self.extract_author(driver)

        df_comments = self.extract_comments_data(driver, post_id)

        if self.db_client and df_comments is not None:
            with self.db_client as db_client:
                db_client.insert_many_data(config.COMMENTS_COLLECTION, df_comments.to_dicts())
                logger.debug(f"Comments saved for post: {post_id}")

                db_client.insert_many_data(config.POSTS_COLLECTION, pl.DataFrame([
                    {'post_id': post_id, 'author': author, 'subreddit': subreddit, 'title': title,
                     'permalink': href}]).to_dicts())
                logger.debug(f"Post saved for subreddit: {subreddit}")

    def extract_comments_data(self, driver, post_id):
        """
        Extract comments data from post
        :param driver: Driver
        :param post_id: post id
        :return: comments data or None if not found
        """
        try:
            scroll_to_bottom(driver, 1)  # Scroll to bottom to load more comments per post

            comments = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//shreddit-comment[not(@is-comment-deleted) and not(@is-author-deleted)]")))
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"WebDriver error while getting comments: {str(e)}")
            logger.warning(f"Comments not found for post: {post_id}. Continue with next.")
            return None

        except Exception as e:
            logger.error(f"Unknown error while getting comments: {str(e)}")
            logger.warning(f"Error for post: {post_id}. Continue with next.")
            return None

        comments_data = self.process_comments(comments, post_id)

        # Remove duplicated comments based on text
        comments_data = comments_data.unique(subset=["text"])
        return comments_data

    @staticmethod
    def extract_author(driver):
        """
        Extract author from post
        :param driver: driver
        :return: author or empty string if not found
        """
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'author-name')]")))
            return driver.find_element(By.XPATH, "//a[contains(@class, 'author-name')]").text
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"NoSuchElementException while getting author: {str(e)}")
            return ''
        except Exception as e:
            logger.error(f"Unknown error while getting author: {str(e)}")
            return ''

    @staticmethod
    def process_comments(comments, post_id):
        """
        Process comments and return a DataFrame with the data
        :param comments: Comments to process
        :param post_id: post id (relevant for logging)
        :return: DataFrame with comments data
        """
        df_comments = pl.DataFrame(
            schema={'post_id': pl.Utf8, 'text': pl.Utf8, 'subreddit': pl.Utf8, 'author': pl.Utf8, 'upvotes': pl.Int64,
                    'thing_id': pl.Utf8, 'parent_id': pl.Utf8})

        for i, comment in enumerate(comments):
            try:
                WebDriverWait(comment, 5).until(
                    EC.presence_of_element_located((By.XPATH, ".//div[@id='-post-rtjson-content']/p")))
                text = comment.find_element(By.XPATH, ".//div[@id='-post-rtjson-content']/p").text

                if text is None:
                    logger.warning(f"Skipping comment {i + 1} of {len(comments)} as it has no text, post: {post_id}")
                    continue

                df_comments = pl.concat([df_comments, SubredditScraper.extract_comment_data(comment, post_id, text)])

            except NoSuchElementException as e:
                logger.error(f"NoSuchElementException while processing comment: {str(e)}")
                continue
            except Exception as e:
                logger.error(f"Unknown error while processing comment: {str(e)}")
                logger.warning(f"Skipping comment {i + 1} of {len(comments)}, post: {post_id}")
                continue

        return df_comments

    @staticmethod
    def extract_comment_data(comment, post_id, text):
        """
        Extracts comment data from a comment element
        :param comment: Comment element
        :param post_id: post id
        :param text: text of the comment
        :return: DataFrame with comment data
        """
        try:
            author = comment.get_attribute("author")
            thing_id = comment.get_attribute("thingid")
            parent_id = comment.get_attribute("parentid") if comment.get_attribute("parentid") else ""
            up_votes = int(comment.get_attribute("score")) if comment.get_attribute("score") else 0
            subreddit = comment.get_attribute("permalink").split("/")[2]

            return pl.DataFrame([{'post_id': post_id, 'text': text, 'subreddit': subreddit, 'author': author,
                                  'upvotes': up_votes, 'thing_id': thing_id, 'parent_id': parent_id}])
        except Exception as e:
            logger.error(f"Error while extracting comment data: {str(e)}")
            return pl.DataFrame()

    @staticmethod
    def get_subreddit_url(subreddit_id):
        return f'https://www.reddit.com/r/{subreddit_id}'
