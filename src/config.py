from selenium.webdriver.firefox.options import Options
from utils import is_running_in_docker

# Selenium Driver
DRIVER_OPTIONS = Options()
DRIVER_OPTIONS.add_argument('-headless')
DRIVER_OPTIONS.add_argument('-no-sandbox')
DRIVER_OPTIONS.set_preference("profile.managed_default_content_settings.images", 2)

# Scraping
SCROLL_TIME = 10
SENTIMENT_ANALYSIS = False

# DB
MONGODB_URI = "mongodb://localhost:27017/" if not is_running_in_docker() else "mongodb://mongodb:27017/"
DATABASE_NAME = "reddit_sentiment"
POSTS_COLLECTION = "posts"
COMMENTS_COLLECTION = "comments"
