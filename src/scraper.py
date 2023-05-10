import logging

import polars as pl
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm

from src import config
from src.utils import get_driver, handle_cookie_banner, scroll_to_bottom

logger = logging.getLogger(__name__)


class SubredditScraper:
    def __init__(self, driver_options, db_client):
        self.driver_options = driver_options
        self.db_client = db_client

    def scrape_subreddit(self, subreddit_id, max_posts=None):
        with get_driver(self.driver_options) as driver:
            driver.get(self.get_subreddit_url(subreddit_id))
            WebDriverWait(driver, 10).until(EC.url_matches(r"https://www.reddit.com/r/.*"))

            handle_cookie_banner(driver)

            logger.info(f"Scrolling {config.SCROLL_TIME} seconds...")
            scroll_to_bottom(driver, config.SCROLL_TIME)
            logger.info("Scrolling finished")

            self.extract_post_data(driver, max_posts)

    def extract_post_data(self, driver, max_posts=None):
        post_elements = driver.find_elements(By.XPATH, "//div[@data-testid='post-container']//a[@data-click-id='body']")
        post_hrefs = [element.get_attribute('href') for element in post_elements]

        logger.info(f"Found {len(post_hrefs)} posts")

        if max_posts:
            logger.info(f"Limiting posts to {max_posts}")
            post_hrefs = post_hrefs[:max_posts]

        count = 1
        for href in tqdm(post_hrefs, desc="Processing posts"):
            try:
                driver.get(href)
            except Exception as e:
                logger.error(f"Error while getting href: {href}, {str(e)} continue with next.")
                driver.close()
                continue

            logger.debug(f"Post {count} of {len(post_hrefs)}")
            logger.debug(f"URL: {href}")
            count += 1

            split_url = href.split('/')

            post_id = split_url[6]
            subreddit = split_url[4]
            title = split_url[7]
            WebDriverWait(driver, 10).until(EC.url_contains(subreddit))

            author = ''

            # Extract the author but add WebDriverWait to ensure it's loaded
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'author-name')]")))
                author = driver.find_element(By.XPATH, "//a[contains(@class, 'author-name')]").text
            except Exception as e:
                logger.error(f"Error while getting author: {str(e)}")

            # Extract and save comments
            df_comments = self.extract_comments_data(driver, post_id)

            if self.db_client:
                with self.db_client as db_client:
                    db_client.insert_many_data(config.COMMENTS_COLLECTION, df_comments.to_dicts())
                    logger.info(f"Comments saved for post: {post_id}")

                    # Save post
                    db_client.insert_many_data(config.POSTS_COLLECTION, pl.DataFrame([
                        {'post_id': post_id, 'author': author, 'subreddit': subreddit, 'title': title,
                         'permalink': href}]).to_dicts())
                    logger.info(f"Post saved for subreddit: {subreddit}")

    @staticmethod
    def extract_comments_data(driver, post_id):
        # print(driver.current_url)

        scroll_to_bottom(driver, 1)  # Scroll to bottom to load more comments per post

        try:
            comments = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "shreddit-comment")))
        except Exception as e:
            logger.error(f"Error while getting comments: {str(e)}")
            return pl.DataFrame(
                schema={'id': pl.Utf8, 'text': pl.Utf8, 'subreddit': pl.Utf8, 'author': pl.Utf8, 'upvotes': pl.Int64,
                        'thing_id': pl.Utf8, 'parent_id': pl.Utf8})

        df_comments = pl.DataFrame(
            schema={'post_id': pl.Utf8, 'text': pl.Utf8, 'subreddit': pl.Utf8, 'author': pl.Utf8, 'upvotes': pl.Int64,
                    'thing_id': pl.Utf8, 'parent_id': pl.Utf8})

        count = 1

        for comment in tqdm(comments, desc=f"Processing '{post_id}' comments", leave=False):

            try:
                WebDriverWait(comment, 5).until(
                    EC.presence_of_element_located((By.XPATH, ".//div[@id='-post-rtjson-content']/p")))
            except Exception as e:
                logger.error(f"Error while getting comment text: {str(e)}")
                continue

            text = comment.find_element(By.XPATH, ".//div[@id='-post-rtjson-content']/p").text
            if text:

                try:
                    # Extract the author
                    author = comment.get_attribute("author")

                    # id of comment named 'thing' by Reddit
                    thing_id = comment.get_attribute("thingid")

                    # check parent id if it exists
                    parent_id = ""
                    if comment.get_attribute("parentid"):
                        parent_id = comment.get_attribute("parentid")  # print(f"Parent id: {parent_id}")

                    # Extract the upvotes (score)
                    up_votes = int(comment.get_attribute("score")) if comment.get_attribute("score") else 0

                    # Extract the permalink and split to get the subreddit
                    permalink = comment.get_attribute("permalink")
                    # print(f"Permalink: {permalink}")
                    subreddit = permalink.split("/")[2]

                    # print(f"Comment {count} of {len(comments)}")
                    count += 1

                    # print(f"Text: {text}")
                    # print(f"Author: {author}")
                    # print(f"Post id: {post_id}")
                    # print(f"Thing id: {thing_id}")
                    # print('\n')

                    df_comments = pl.concat([df_comments, pl.DataFrame([{'post_id': post_id, 'text': text,
                                                                         'subreddit': subreddit, 'author': author,
                                                                         'upvotes': up_votes, 'thing_id': thing_id,
                                                                         'parent_id': parent_id}])])
                except Exception as e:
                    logger.error(f"Error while getting comment data: {str(e)}")
                    continue

        return df_comments

    @staticmethod
    def save_data_to_parquet(df, file_name):
        df.write_parquet(file_name, compression='snappy')

    @staticmethod
    def save_data_to_csv(df, file_name):
        # save polars to csv in current directory
        df.write_csv(file_name)

    @staticmethod
    def get_subreddit_url(subreddit_id):
        return f'https://www.reddit.com/r/{subreddit_id}'
