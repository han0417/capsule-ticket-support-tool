from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bot.form import PAGE_LOAD_TIMEOUT


def start() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    return driver
