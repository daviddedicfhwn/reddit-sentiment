"""Configurations for reddit sentiment analysis."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_driver_options():
    """Configure selenium driver options."""
    from selenium.webdriver.firefox.options import Options
    options = Options()
    options.add_argument('-headless')
    options.add_argument('-no-sandbox')
    options.set_preference("profile.managed_default_content_settings.images", 2)
    return options


# Selenium Driver
DRIVER_OPTIONS = get_driver_options()

# Scraping
SCROLL_TIME = int(os.getenv("SCROLL_TIME", 10))  # Time in seconds to scroll on a page to load more posts
MAX_POSTS_PER_SUBREDDIT = os.getenv("MAX_POSTS_PER_SUBREDDIT")  # None for no limit, else specify number

# DB
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "reddit_sentiment")
POSTS_COLLECTION = os.getenv("POSTS_COLLECTION", "posts")
COMMENTS_COLLECTION = os.getenv("COMMENTS_COLLECTION", "comments")

# Sentiment Analysis
SENTIMENT_ANALYSIS = os.getenv("SENTIMENT_ANALYSIS", True)  # Enable sentiment analysis or not
SENTIMENT_FEATURES = [(POSTS_COLLECTION, 'title'), (COMMENTS_COLLECTION, 'text')]
SENTIMENT_MODEL = os.getenv("SENTIMENT_MODEL", "cardiffnlp/twitter-xlm-roberta-base-sentiment")
