import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException

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
NEXT_MONTH_BTN = (By.ID, "moveNextMonth")
CAL_YEAR_MONTH = (By.ID, "sdYearMonth")
TIME_SELECT_BOX = (By.CSS_SELECTOR, "div.time-select")


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


def _select_date(driver, day: int = 21) -> None:
    current_ym = WebDriverWait(driver, ELEMENT_TIMEOUT).until(
        EC.presence_of_element_located(CAL_YEAR_MONTH)
    ).get_attribute("value")

    WebDriverWait(driver, ELEMENT_TIMEOUT).until(
        EC.element_to_be_clickable(NEXT_MONTH_BTN)
    ).click()

    # 等隱藏 input 的 value 從舊月份切換到新月份
    WebDriverWait(driver, ELEMENT_TIMEOUT).until(
        lambda d: d.find_element(*CAL_YEAR_MONTH).get_attribute("value") != current_ym
    )

    yyyymm = driver.find_element(*CAL_YEAR_MONTH).get_attribute("value")
    day_id = f"{yyyymm}{day:02d}"

    # 等到日期元素同時存在且帶有 live class（AJAX 更新後才會出現）
    try:
        day_el = WebDriverWait(driver, AJAX_TIMEOUT).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, f"a.live[id='{day_id}']")
            )
        )
    except Exception:
        raise ValueError(f"日期 {day_id} 目前無法購票（等待 {AJAX_TIMEOUT}s 後仍非開放狀態）")

    driver.execute_script("arguments[0].click();", day_el)

    # 點擊後等一下，偵測網站是否彈出 alert（例如：This schedule has been sold out）
    time.sleep(0.5)
    try:
        alert = driver.switch_to.alert
        msg = alert.text
        alert.dismiss()
        raise ValueError(f"日期 {day_id} 點擊後出現提示：{msg}")
    except NoAlertPresentException:
        pass


def _select_timeslot(driver, target_time: str = "14:00") -> None:
    # 點擊下拉展開時段選單
    WebDriverWait(driver, AJAX_TIMEOUT).until(
        EC.element_to_be_clickable(TIME_SELECT_BOX)
    ).click()

    # 等到有包含目標時間且非 soldout 的 <li> 變為可點擊
    try:
        slot = WebDriverWait(driver, AJAX_TIMEOUT).until(
            EC.element_to_be_clickable((
                By.XPATH,
                f"//li[@data-id='sdSeq' and not(contains(@class,'soldout')) and contains(.,'{target_time}')]"
            ))
        )
    except Exception:
        raise ValueError(f"時段 {target_time} 目前無法購票或不存在")

    driver.execute_script("arguments[0].click();", slot)


def fill(driver, config: dict) -> None:
    driver.get(config["url"])
    _wait_and_fill(driver, NAME_SELECTOR, config["name"])
    _wait_and_fill(driver, EMAIL_SELECTOR, config["email"])
    _wait_and_fill(driver, PASSWORD_SELECTOR, config["password"])
    _select_nationality(driver)
    _check(driver, AGREE_ALL)
    _check(driver, AGREE5)
    _select_date(driver, day=config["day"])
