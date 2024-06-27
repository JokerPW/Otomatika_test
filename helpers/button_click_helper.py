from RPA.Browser.Selenium import Selenium
from RPA.Browser.Selenium import ElementNotFound

def click_button_by_title(browser, element_name):
    try:
        browser.click_button("css:button[title='" + element_name + "']")
    except ElementNotFound as e:
        print ("Element not found")

def click_button_by_class(driver, element_name):
    try:
        driver.click_button("css:." + element_name)
    except ElementNotFound as e:
        print ("Element not found")


def click_button_by_label(driver, element_name):
    try:
        driver.click_button("xpath://button[normalize-space()='" + element_name + "']")
    except ElementNotFound as e:
        print ("Element not found")


def default_case():
    return "Element type not found"


def click_button_by (driver, element_type, element_name):
    switcher = {
        "title": click_button_by_title,
        "class": click_button_by_class,
        "label": click_button_by_label,
    }
    # Get the function from switcher dictionary
    func = switcher.get(element_type, default_case)
    # Execute the function
    return func(driver, element_name)