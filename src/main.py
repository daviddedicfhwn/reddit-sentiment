import config
import database
from scraper import SubredditScraper
from sentiment_pipeline import SentimentPipeline

import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("scraping.log"), logging.StreamHandler()])

logger = logging.getLogger(__name__)


def main():
    database.connect_to_db()

    subreddit_list = ['popular']
    logger.debug(f"Subreddit list: {subreddit_list}")

    scraper = SubredditScraper(config.DRIVER_OPTIONS)

    for subreddit in subreddit_list:
        logger.info(f"Scraping subreddit: {subreddit}")
        scraper.scrape_subreddit(subreddit)

    database.close_db_connection()


if __name__ == '__main__':
    main()
