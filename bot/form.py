from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# driver.get() 等待整個頁面載入完成的上限（秒）
# 搶票當下伺服器可能很忙，網頁需要 3~4 分鐘才跑好，設保守一點
PAGE_LOAD_TIMEOUT = 300

# 等頁面上「已存在」的欄位變為可互動的上限（秒）
# 適用於：姓名、Email、密碼、國籍選單 ── 頁面載完後這些幾乎立刻出現
ELEMENT_TIMEOUT = 30

# 等 AJAX 動態載入的選項出現的上限（秒）
# 適用於：付款方式清單 ── 需要額外一次 API 請求才會填進去
AJAX_TIMEOUT = 60

NAME_SELECTOR = (By.ID, "rsBuyerName")
EMAIL_SELECTOR = (By.ID, "email")
PASSWORD_SELECTOR = (By.ID, "rsBuyerPwd")
NATIONAL_SELECTBOX = (By.ID, "nationalSelectbox")
NATIONAL_TAIWAN = (By.CSS_SELECTOR, "li[data-id='national'][data-value='TAIWAN']")
AGREE_ALL = (By.ID, "agreeAll")
AGREE5 = (By.ID, "agree5")
PAY_METHOD_AREA = (By.ID, "payMethodArea")
PAY_OVERSEAS = (By.XPATH, "//div[@id='payMethodArea']//li[contains(., 'Overseas')]")


def _wait_and_fill(driver, selector: tuple, value: str) -> None:
    element = WebDriverWait(driver, ELEMENT_TIMEOUT).until(
        EC.visibility_of_element_located(selector)
    )
    element.clear()
    element.send_keys(value)


def _select_nationality(driver) -> None:
    WebDriverWait(driver, ELEMENT_TIMEOUT).until(
        EC.element_to_be_clickable(NATIONAL_SELECTBOX)
    ).click()
    WebDriverWait(driver, ELEMENT_TIMEOUT).until(
        EC.element_to_be_clickable(NATIONAL_TAIWAN)
    ).click()


def _check(driver, selector: tuple) -> None:
    element = WebDriverWait(driver, ELEMENT_TIMEOUT).until(
        EC.presence_of_element_located(selector)
    )
    if not element.is_selected():
        driver.execute_script("arguments[0].click();", element)


def _select_payment(driver) -> None:
    # 點開選單，觸發 AJAX 載入付款選項
    WebDriverWait(driver, ELEMENT_TIMEOUT).until(
        EC.element_to_be_clickable(PAY_METHOD_AREA)
    ).click()
    # 等 Overseas 選項出現
    li = WebDriverWait(driver, AJAX_TIMEOUT).until(
        EC.presence_of_element_located(PAY_OVERSEAS)
    )
    # 讀出實際的 data-value（AJAX 載入後才會有）
    data_value = li.get_attribute("data-value")
    label = li.text.strip()
    # 直接寫入隱藏欄位並觸發驗證，繞過 jQuery 事件委派
    driver.execute_script("""
        $('#payMethod').val(arguments[0]);
        $('#payMethodArea .placeholder').text(arguments[1]);
        $('#payMethodArea').removeClass('on');
        if (typeof valueCheck === 'function') valueCheck();
    """, data_value, label)


def fill(driver, config: dict) -> None:
    driver.get(config["url"])
    _wait_and_fill(driver, NAME_SELECTOR, config["name"])
    _wait_and_fill(driver, EMAIL_SELECTOR, config["email"])
    _wait_and_fill(driver, PASSWORD_SELECTOR, config["password"])
    _select_nationality(driver)
    _check(driver, AGREE_ALL)
    _check(driver, AGREE5)
    _select_payment(driver)
