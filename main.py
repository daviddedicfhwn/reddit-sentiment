import logging

from src.config import MAX_POSTS_PER_SUBREDDIT, SUBREDDIT_LIST, DRIVER_OPTIONS, SENTIMENT_ANALYSIS, SENTIMENT_FEATURES
from src.database import MongoDBClient
from src.scraper import SubredditScraper
from src.sentiment_controller import SentimentController

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("scraping.log"), logging.StreamHandler()])

logger = logging.getLogger(__name__)


def main():
    logger.debug(f"Subreddit list: {SUBREDDIT_LIST}")

    db_client = MongoDBClient()
    scraper = SubredditScraper(DRIVER_OPTIONS, db_client)

    for subreddit in SUBREDDIT_LIST:
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
