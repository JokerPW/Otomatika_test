from RPA.Browser.Selenium import Selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from robocorp.tasks import get_output_dir, task
from helpers.button_click_helper import click_button_by
import time

FILE_NAME = "otomatila.xlsx"
NEWS_URL = "https://gothamist.com/"
BROWSER = Selenium()
#OUTPUT_DIR = Path(os.getenv("ROBOT_ARTIFACTS", "output"))

POPUP_CLOSE_BTN = "Close"
POPUP_CLOSE_BTN_TAG_TYPE = "title"

SEARCH_BTN = "-mr-2"
SEARCH_BTN_TAG_TYPE = "class"

INPUT_NAME = "q"

GO_SEARCH = 'search-page-button'
GO_SEARCH_BTN_TAG_TYPE = "class"


def retrieve_webpage(your_url):
    """Access website with the given URL and return its page"""
    BROWSER.open_available_browser(your_url)


def close_popup(button_tag, tag_type):
    click_button_by (BROWSER, tag_type, button_tag)


def open_search(button_tag, tag_type):
    click_button_by (BROWSER, tag_type, button_tag)


def search_given_words(input_name, words):
    # input class: search-page-input
    # input selector: #search > input
    inputElement = BROWSER.input_text("css:input[name='" + input_name + "']", words)
    click_button_by (BROWSER, GO_SEARCH_BTN_TAG_TYPE, GO_SEARCH)
    

@task
def minimal_task():
    """Code for Otomatika assignment test"""

    retrieve_webpage(NEWS_URL)
    time.sleep(2)
    close_popup(POPUP_CLOSE_BTN, POPUP_CLOSE_BTN_TAG_TYPE)
    time.sleep(2)
    open_search(SEARCH_BTN, SEARCH_BTN_TAG_TYPE)
    time.sleep(2)
    search_given_words(INPUT_NAME, "test")

