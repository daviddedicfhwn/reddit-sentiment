from src.utils import is_running_in_docker


def get_driver_options():
    from selenium.webdriver.firefox.options import Options

    """
    Returns the Firefox webdriver options.

    :return: Firefox webdriver options.
    """
    options = Options()
    options.add_argument('-headless')
    options.add_argument('-no-sandbox')
    options.set_preference("profile.managed_default_content_settings.images", 2)
    return options


# Selenium Driver
DRIVER_OPTIONS = get_driver_options()

# Scraping
SCROLL_TIME = 10  # see README.md for more information

SUBREDDIT_LIST = ['popular']
SUBREDDIT_FILE = "./data/subreddits.json"

MAX_POSTS_PER_SUBREDDIT = None  # None for no limit

# DB
MONGODB_URI = "mongodb://localhost:27017/" if not is_running_in_docker() else "mongodb://mongodb:27017/"
DATABASE_NAME = "reddit_sentiment"
POSTS_COLLECTION = "posts"
COMMENTS_COLLECTION = "comments"

# Sentiment Analysis
SENTIMENT_ANALYSIS = True
SENTIMENT_FEATURES = [(POSTS_COLLECTION, 'title'), (COMMENTS_COLLECTION, 'text')]
SENTIMENT_MODEL = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
