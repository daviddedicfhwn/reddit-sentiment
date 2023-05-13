import logging
import argparse

from src.config import MAX_POSTS_PER_SUBREDDIT, DRIVER_OPTIONS, SENTIMENT_ANALYSIS, SENTIMENT_FEATURES, SUBREDDIT_FILE, \
    SUBREDDIT_LIST
from src.database import MongoDBClient
from src.scraper import SubredditScraper
from src.sentiment_controller import SentimentController
from src.utils import get_subreddits_from_file

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("scraping.log"), logging.StreamHandler()])

logger = logging.getLogger(__name__)


def main():
    args = get_args()
    if args.sentiment_only:
        logger.info("Running sentiment analysis only")
        sentiment_analysis()
        return

    scrape_subreddits()

    if SENTIMENT_ANALYSIS:
        sentiment_analysis()


def scrape_subreddits():
    logger.info("Scraper starting")

    db_client = MongoDBClient()
    with db_client as db_client:
        db_client.db.list_collection_names()
        logger.info(f"DB connection established")

    subreddit_list = get_subreddits_from_file(SUBREDDIT_FILE)
    if not subreddit_list:
        logger.warning(f"File '{SUBREDDIT_FILE}' does not exist. Using config list instead.")
        subreddit_list = SUBREDDIT_LIST
    logger.info(f"Subreddits to scrape: {subreddit_list}")

    scraper = SubredditScraper(DRIVER_OPTIONS, db_client)
    for subreddit in subreddit_list:
        logger.info(f"Scraping subreddit: {subreddit}")
        scraper.scrape_subreddit(subreddit, max_posts=MAX_POSTS_PER_SUBREDDIT)

    logger.info("Scraping complete")


def sentiment_analysis():
    logger.info("Performing sentiment analysis")

    db_client = MongoDBClient()

    sentiment_controller = SentimentController(db_client)
    for collection, field in SENTIMENT_FEATURES:
        logger.info(f"Sentiment analysis for {collection} - {field}")
        sentiment_controller.write_sentiments_to_documents(collection=collection, field_to_analyze=field)
    logger.info("Sentiment analysis complete")


def get_args():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--sentiment-only', action='store_true')
        return parser.parse_args()
    except Exception as e:
        return None


if __name__ == '__main__':
    main()
