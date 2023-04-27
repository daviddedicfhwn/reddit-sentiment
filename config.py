from selenium.webdriver.firefox.options import Options

DRIVER_OPTIONS = Options()
DRIVER_OPTIONS.add_argument('-headless')
DRIVER_OPTIONS.add_argument('-no-sandbox')
DRIVER_OPTIONS.set_preference("profile.managed_default_content_settings.images", 2)

SCROLL_TIME = 1
SENTIMENT_ANALYSIS = False

