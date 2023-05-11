import json
import logging
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

logger = logging.getLogger(__name__)


def is_running_in_docker():
    """
    Checks if the current process is running inside a Docker container
    :return: True if running inside a Docker container, False otherwise
    """
    return os.environ.get('DOCKER_CONTAINER') is not None


def get_subreddits_from_file(filename):
    """
    Gets the list of subreddits from the JSON file if it exists.

    If the file does not exist, None is returned.

    :param filename: The name of the JSON file to load (default is "subreddits.json").
    :return: The JSON file as a Python dictionary.
    """

    # filename is a relative path, so we need to get the absolute path
    if not os.path.isfile(filename):
        return None

    with open(filename, "r") as file:
        json_file = json.load(file)

    return json_file


def get_driver(driver_options):
    """
    Returns an instance of the Firefox webdriver with the given options.

    :param driver_options: Firefox webdriver options.
    :return: Firefox webdriver instance.
    """
    if is_running_in_docker():
        logger.info("Running in Docker container, using remote webdriver")
        return webdriver.Remote(command_executor='http://selenium-hub:4444/wd/hub', options=driver_options)

    return webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=driver_options)


def handle_cookie_banner(driver):
    """
    Handles the cookie banner on the Reddit page by clicking the "Accept All" button.

    :param driver: Webdriver instance.
    """
    try:
        # Find the element by XPATH
        # fixme cookie
        section = driver.find_element(By.XPATH,
                                      "//span[contains(., 'Cookie') or contains(., 'cookies') or contains(., 'Technologien')]")
        parent_element = section.find_element(By.XPATH, "./ancestor::section[2]")
        button = parent_element.find_element(By.XPATH,
                                             ".//button[contains(text(), 'Alle akzeptieren') or contains(text(), 'Accept All')]")
        button.click()

        logger.debug("Cookie banner handled")
    except Exception as e:
        logger.error(f"Error while handling cookie banner: {str(e)}")
        pass


def scroll_to_bottom(driver, scroll_time):
    """
    Scrolls to the bottom of the page repeatedly for a specified amount of time.

    :param driver: Webdriver instance.
    :param scroll_time: Time in seconds for scrolling.
    """
    start_time = time.time()

    while time.time() - start_time < scroll_time:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def handle_google_credential(driver):
    """
    Handles the Google Credential popup by clicking the "Close" button.

    :param driver: Webdriver instance.
    """
    try:
        # Find the element by ID
        credential_container = driver.find_element(By.ID, "credential_picker_container")

        # Switch to the iframe
        iframe = credential_container.find_element(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframe)

        # Find the "Close" button and click it
        close_button = driver.find_element(By.XPATH, "//button[@aria-label='Close']")
        close_button.click()

        # Switch back to the default content
        driver.switch_to.default_content()

        logger.debug("Google Credential handled")
    except Exception as e:
        logger.debug("No Google Credential", str(e))
        pass
