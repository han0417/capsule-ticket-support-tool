from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def start() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(options=options)
