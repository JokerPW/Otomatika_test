from RPA.Browser.Selenium import Selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from SeleniumLibrary.errors import ElementNotFound
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from robocorp.tasks import get_output_dir, task
from helpers.button_click_helper import click_button_by
import time

FILE_NAME = "otomatila.xlsx"
NEWS_URL = "https://gothamist.com/"
BROWSER = Selenium()
NEWS_LIST = []
#OUTPUT_DIR = Path(os.getenv("ROBOT_ARTIFACTS", "output"))
SEARCH_WORDS = "germany"
MONEY_WORDS = ["$", "dollar", "dollars", "USD"]

POPUP_CLOSE_BTN = "Close"
POPUP_CLOSE_BTN_TAG_TYPE = "title"

SEARCH_BTN = "-mr-2"
SEARCH_BTN_TAG_TYPE = "class"

INPUT_NAME = "q"

GO_SEARCH = 'search-page-button'
GO_SEARCH_BTN_TAG_TYPE = "class"

NEWS_CLASS = 'v-card'
NEWS_XPATH = '/html/body/div[1]/div/div/main/div[2]/div/section[2]/div/div[1]/div[2]/div[@]/div'
CHAR_TO_REPLACE = "@"
PICTURE_XPATH = '//*[@id="resultList"]/div[2]/div[1]/div/div[1]/figure[2]/div/div/a/div/img'

def retrieve_webpage(your_url):
    """Access website with the given URL and return its page"""
    BROWSER.open_available_browser(your_url)


def close_popup(button_tag, tag_type):
    click_button_by (BROWSER, tag_type, button_tag)


def open_search(button_tag, tag_type):
    click_button_by (BROWSER, tag_type, button_tag)


def search_given_words(input_name, words):
    inputElement = BROWSER.input_text("css:input[name='" + input_name + "']", words)
    click_button_by (BROWSER, GO_SEARCH_BTN_TAG_TYPE, GO_SEARCH)


def retrieve_news(full_xpath, char_to_replace, replacement_char):
    xpath = full_xpath.replace(char_to_replace, replacement_char, 1)
    ret = None
    try:
        ret = BROWSER.find_element("xpath:" + xpath)
    except ElementNotFound:
        print("element not found")
    
    return ret


def count_occurrences(search, title, description):
    count = 0
    words = search.split(' ')
    for word in words:
        if word in title or word in description:
            count = count + 1

    return count


def check_for_money(search, title, description):
    for word in search:
        if word in title or word in description:
            return True
        
    return False


def loop_through_news(news_class, news_xpath):
    # Wait until the search results are present
    wait = WebDriverWait(BROWSER.driver, 20)
    search_results = wait.until(EC.presence_of_element_located((By.CLASS_NAME, news_class)))

    items = []
    iter = 1

    item = retrieve_news(news_xpath, CHAR_TO_REPLACE, str(iter))
    while item is not None:
        items.append(item)
        iter = iter + 1
        item = retrieve_news(news_xpath, CHAR_TO_REPLACE, str(iter))

    for item in items:
        try:
            element = item.find_element(By.CLASS_NAME, 'h2')
            title = element.text
            element = item.find_element(By.CLASS_NAME, 'desc')
            description = element.text
            element = item.find_element(By.XPATH, PICTURE_XPATH)
            picture = element.get_attribute("src")
            count = count_occurrences(SEARCH_WORDS, title, description)
            contains_money = check_for_money(MONEY_WORDS, title, description)

        except:
            print("element not found in this item.")


@task
def minimal_task():
    """Code for Otomatika assignment test"""

    retrieve_webpage(NEWS_URL)
    time.sleep(2)
    close_popup(POPUP_CLOSE_BTN, POPUP_CLOSE_BTN_TAG_TYPE)
    time.sleep(2)
    open_search(SEARCH_BTN, SEARCH_BTN_TAG_TYPE)
    time.sleep(2)
    search_given_words(INPUT_NAME, SEARCH_WORDS)
    time.sleep(20)
    loop_through_news(NEWS_CLASS, NEWS_XPATH)

