import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager

def get_driver(driver_options):
    """
    Returns an instance of the Firefox webdriver with the given options.

    :param driver_options: Firefox webdriver options.
    :return: Firefox webdriver instance.
    """
    return webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=driver_options)

def handle_cookie_banner(driver):
    """
    Handles the cookie banner on the Reddit page by clicking the "Accept All" button.

    :param driver: Webdriver instance.
    """
    try:
        # Find the element by XPATH
        section = driver.find_element(By.XPATH, "//span[contains(., 'Cookies') or contains(., 'Technologien')]")
        parent_element = section.find_element(By.XPATH, "./ancestor::section[2]")
        button = parent_element.find_element(By.XPATH, ".//button[contains(text(), 'Alle akzeptieren') or contains(text(), 'Accept All')]")
        button.click()

        print("Cookie banner handled")
    except Exception as e:
        print("No cookie banner", str(e))
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

        print("Google Credential handled")
    except Exception as e:
        print("No Google Credential popup", str(e))
        pass
