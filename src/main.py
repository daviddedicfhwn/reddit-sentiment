import logging

import config
from scraper import SubredditScraper
from sentiment_controller import SentimentController

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("scraping.log"), logging.StreamHandler()])

logger = logging.getLogger(__name__)


def main():
    logger.debug(f"Subreddit list: {config.SUBREDDIT_LIST}")

    scraper = SubredditScraper(config.DRIVER_OPTIONS)

    for subreddit in config.SUBREDDIT_LIST:
        logger.info(f"Scraping subreddit: {subreddit}")
        scraper.scrape_subreddit(subreddit, max_posts=config.MAX_POSTS_PER_SUBREDDIT)

    logger.info("Scraping complete")

    if config.SENTIMENT_ANALYSIS:
        logger.info("Performing sentiment analysis")
        sentiment_controller = SentimentController()

        for collection, field in config.SENTIMENT_FEATURES:
            logger.info(f"Sentiment analysis for {collection} - {field}")
            sentiment_controller.write_sentiments_to_documents(collection=collection, field_to_analyze=field)

        logger.info("Sentiment analysis complete")


if __name__ == '__main__':
    main()
