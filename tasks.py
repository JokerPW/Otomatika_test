from pathlib import Path
import time
import logging

from robocorp import workitems
from robocorp.tasks import get_output_dir, task

from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files as Excel
from RPA.Robocloud.Items import Items

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from SeleniumLibrary.errors import ElementNotFound
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers.button_click_helper import click_button_by
from model.news_model import NewsModel


logger = logging.getLogger(__name__)
FILE_NAME = "otomatila.xlsx"
NEWS_URL = "https://gothamist.com/"
BROWSER = Selenium()
NEWS_LIST = []
OUTPUT_DIR = get_output_dir() or Path("output")

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


def load_robocloud_parameters():
    search_words = "test"
    section = "test"
    months = "0"
    
    try:
        print ("Loading parameters")
        items = Items()
        items = items.get_work_item_payload()

        search_words = items.get("search_phrase")
        section = items.get("section")
        months = items.get("months")
    
    except RuntimeError as re:
        logger.exception("Unable to load parameters")
        logger.exception (re)
    
    return search_words, section, months


def retrieve_webpage(your_url):
    BROWSER.open_available_browser(your_url)


def close_popup(button_tag, tag_type, logger):
    click_button_by (BROWSER, tag_type, button_tag)


def open_search(button_tag, tag_type, logger):
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
        logger.exception("element not found")
    
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


def loop_through_news(search_words, news_class, news_xpath):
    # Wait until the search results are present
    wait = WebDriverWait(BROWSER.driver, 20)
    search_results = wait.until(EC.presence_of_element_located((By.CLASS_NAME, news_class)))

    news_items = []
    iter = 1

    item = retrieve_news(news_xpath, CHAR_TO_REPLACE, str(iter))
    while item is not None:
        iter = iter + 1
        item = retrieve_news(news_xpath, CHAR_TO_REPLACE, str(iter))

        try:
            element = item.find_element(By.CLASS_NAME, 'h2')
            title = element.text
            element = item.find_element(By.CLASS_NAME, 'desc')
            description = element.text
            element = item.find_element(By.XPATH, PICTURE_XPATH)
            picture = element.get_attribute("src")
            count = count_occurrences(search_words, title, description)
            contains_money = check_for_money(MONEY_WORDS, title, description)
            news_items.append(NewsModel(title, None, description, picture, count, contains_money))
            logger.info("-----------News-----------")
            logger.info("Title: " + title)
            logger.info("Description: " + description)
            logger.info("Picture: " + picture)

        except RuntimeError as re:
            logger.exception("element not found in this item.")
            logger.exception (re)
        except AttributeError as ae:
            logger.exception("element not found in this item.")
            logger.exception (ae)

    return news_items


def save_to_excel(news_list):
    try:
        print ("Saving to Excel file")
        excel = Excel()
        excel.create_workbook()
        header = ["Title", "Date", "Description", "Picture", "Count", "Contains Money"]
        excel.append_rows_to_worksheet([header], header=True)

        for news in news_list:
            row = [news.title, news.date, news.description, news.picture, news.count, news.contains_money]
            excel.append_rows_to_worksheet([row], header=False)

        excel.save_workbook("Otomatika.xlsx")
        excel.close_workbook()
    
    except RuntimeError as re:
        logger.exception ("Unable to write XLS")
        logger.exception (re)
    except TypeError as te:
        logger.exception ("Unable to write XLS")
        logger.exception (te)


@task
def minimal_task():
    """Code for Otomatika assignment test"""
    logging.basicConfig(filename='Otomatika.log', level=logging.INFO)
    logger.info('Started')

    search_words, section, months = load_robocloud_parameters()

    retrieve_webpage(NEWS_URL)
    time.sleep(2)
    close_popup(POPUP_CLOSE_BTN, POPUP_CLOSE_BTN_TAG_TYPE, logger)
    time.sleep(2)
    open_search(SEARCH_BTN, SEARCH_BTN_TAG_TYPE, logger)
    time.sleep(2)
    search_given_words(INPUT_NAME, search_words)
    time.sleep(20)
    news_items = loop_through_news(search_words, NEWS_CLASS, NEWS_XPATH)
    save_to_excel(news_items)

    logger.info('Finished')