from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

WAIT_TIMEOUT = 10

NAME_SELECTOR = (By.ID, "rsBuyerName")
EMAIL_SELECTOR = (By.ID, "email")
PASSWORD_SELECTOR = (By.ID, "rsBuyerPwd")
NATIONAL_SELECTBOX = (By.ID, "nationalSelectbox")
NATIONAL_TAIWAN = (By.CSS_SELECTOR, "li[data-id='national'][data-value='TAIWAN']")
AGREE_ALL = (By.ID, "agreeAll")
AGREE5 = (By.ID, "agree5")


def _wait_and_fill(driver, selector: tuple, value: str) -> None:
    element = WebDriverWait(driver, WAIT_TIMEOUT).until(
        EC.visibility_of_element_located(selector)
    )
    element.clear()
    element.send_keys(value)


def _select_nationality(driver) -> None:
    WebDriverWait(driver, WAIT_TIMEOUT).until(
        EC.element_to_be_clickable(NATIONAL_SELECTBOX)
    ).click()
    WebDriverWait(driver, WAIT_TIMEOUT).until(
        EC.element_to_be_clickable(NATIONAL_TAIWAN)
    ).click()


def _check(driver, selector: tuple) -> None:
    element = WebDriverWait(driver, WAIT_TIMEOUT).until(
        EC.element_to_be_clickable(selector)
    )
    if not element.is_selected():
        element.click()


def fill(driver, config: dict) -> None:
    driver.get(config["url"])
    _wait_and_fill(driver, NAME_SELECTOR, config["name"])
    _wait_and_fill(driver, EMAIL_SELECTOR, config["email"])
    _wait_and_fill(driver, PASSWORD_SELECTOR, config["password"])
    _select_nationality(driver)
    _check(driver, AGREE_ALL)
    _check(driver, AGREE5)
