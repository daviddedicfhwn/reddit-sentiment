import logging

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
    subreddit_list = get_subreddits_from_file(SUBREDDIT_FILE)
    if not subreddit_list:
        logger.warning(f"File '{SUBREDDIT_FILE}' does not exist. Using config list instead.")
        subreddit_list = SUBREDDIT_LIST

    logger.info(f"Subreddits to scrape: {subreddit_list}")

    db_client = MongoDBClient()
    scraper = SubredditScraper(DRIVER_OPTIONS, db_client)

    for subreddit in subreddit_list:
        logger.info(f"Scraping subreddit: {subreddit}")
        scraper.scrape_subreddit(subreddit, max_posts=MAX_POSTS_PER_SUBREDDIT)

    logger.info("Scraping complete")

    if SENTIMENT_ANALYSIS:
        logger.info("Performing sentiment analysis")
        sentiment_controller = SentimentController()

        for collection, field in SENTIMENT_FEATURES:
            logger.info(f"Sentiment analysis for {collection} - {field}")
            sentiment_controller.write_sentiments_to_documents(collection=collection, field_to_analyze=field)

        logger.info("Sentiment analysis complete")


if __name__ == '__main__':
    main()
