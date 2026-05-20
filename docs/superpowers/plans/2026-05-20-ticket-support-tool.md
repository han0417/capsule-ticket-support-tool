# 購票輔助工具 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 建立一個 Selenium Python 自動化腳本，從 `.env` 讀取設定，開啟 Chrome 並自動填寫購票頁面的 name/email/password 欄位，填完後等待使用者手動送出。

**Architecture:** `bot/config.py` 負責載入與驗證 `.env`；`bot/browser.py` 啟動 Chrome；`bot/form.py` 執行表單填寫（顯式等待）；`main.py` 協調三者並在填完後暫停等待使用者操作。

**Tech Stack:** Python 3.10+、Selenium 4.x（內建 selenium-manager）、python-dotenv、pytest

---

## 檔案結構總覽

```
capsule-ticket-support-tool/
├── main.py
├── bot/
│   ├── __init__.py
│   ├── config.py
│   ├── browser.py
│   └── form.py
├── tests/
│   ├── __init__.py
│   ├── test_config.py
│   └── test_form.py
├── .env              # 不提交 git
├── .env.example      # 提交 git
├── .gitignore
└── requirements.txt
```

---

### Task 1：檢查目標頁面，記錄欄位 selector

**Files:**
- 無新增檔案，記錄結果供 Task 5 使用

- [ ] **Step 1：用 Chrome 開啟目標網址**

在瀏覽器手動開啟：`https://www.tbluelinepark.com/ticket_eng/GD2000441`

- [ ] **Step 2：找 name 欄位的 selector**

右鍵點擊 name 輸入框 → 「檢查」。在 DevTools 的 Elements 面板，找到 `<input>` 標籤，記下它的 `id`、`name`、或獨特的 `class`。

例如可能是：`input[name="purchaser_name"]` 或 `#buyer_name`

- [ ] **Step 3：找 email 欄位的 selector**

同上方法找 email 輸入框的 selector。

- [ ] **Step 4：找 password 欄位的 selector**

同上方法找 password 輸入框的 selector。

- [ ] **Step 5：記下三個 selector**

把結果記下來，Task 5 的 `bot/form.py` 會用到。格式如下：

```
NAME_SELECTOR     = (By.CSS_SELECTOR, "你找到的 selector")
EMAIL_SELECTOR    = (By.CSS_SELECTOR, "你找到的 selector")
PASSWORD_SELECTOR = (By.CSS_SELECTOR, "你找到的 selector")
```

---

### Task 2：專案骨架與 git 初始化

**Files:**
- Create: `requirements.txt`
- Create: `.env.example`
- Create: `.gitignore`
- Create: `bot/__init__.py`
- Create: `tests/__init__.py`

- [ ] **Step 1：初始化 git**

```bash
git init
```

Expected: `Initialized empty Git repository in .../capsule-ticket-support-tool/.git/`

- [ ] **Step 2：建立 `requirements.txt`**

```
selenium>=4.0.0
python-dotenv>=1.0.0
pytest>=7.0.0
```

- [ ] **Step 3：建立 `.env.example`**

```
TICKET_URL=https://www.tbluelinepark.com/ticket_eng/GD2000441
BUYER_NAME=王小明
BUYER_EMAIL=your_email@example.com
BUYER_PASSWORD=your_password_here
```

- [ ] **Step 4：建立 `.gitignore`**

```
.env
__pycache__/
*.pyc
*.pyo
dist/
build/
*.spec
.DS_Store
```

- [ ] **Step 5：建立空白 `__init__.py`**

建立 `bot/__init__.py`（空白）與 `tests/__init__.py`（空白）。

- [ ] **Step 6：安裝依賴**

```bash
pip install -r requirements.txt
```

Expected: 所有套件安裝成功，無 error。

- [ ] **Step 7：Commit**

```bash
git add requirements.txt .env.example .gitignore bot/__init__.py tests/__init__.py
git commit -m "chore: project scaffolding"
```

---

### Task 3：實作 `bot/config.py`（含測試）

**Files:**
- Create: `bot/config.py`
- Create: `tests/test_config.py`

- [ ] **Step 1：寫失敗的測試**

建立 `tests/test_config.py`：

```python
import pytest
from bot.config import load


def test_load_returns_all_fields(monkeypatch):
    monkeypatch.setenv("TICKET_URL", "https://example.com")
    monkeypatch.setenv("BUYER_NAME", "Test User")
    monkeypatch.setenv("BUYER_EMAIL", "test@example.com")
    monkeypatch.setenv("BUYER_PASSWORD", "secret")
    config = load()
    assert config["url"] == "https://example.com"
    assert config["name"] == "Test User"
    assert config["email"] == "test@example.com"
    assert config["password"] == "secret"


def test_load_exits_when_url_missing(monkeypatch):
    monkeypatch.delenv("TICKET_URL", raising=False)
    monkeypatch.setenv("BUYER_NAME", "Test User")
    monkeypatch.setenv("BUYER_EMAIL", "test@example.com")
    monkeypatch.setenv("BUYER_PASSWORD", "secret")
    with pytest.raises(SystemExit):
        load()


def test_load_exits_when_name_missing(monkeypatch):
    monkeypatch.setenv("TICKET_URL", "https://example.com")
    monkeypatch.delenv("BUYER_NAME", raising=False)
    monkeypatch.setenv("BUYER_EMAIL", "test@example.com")
    monkeypatch.setenv("BUYER_PASSWORD", "secret")
    with pytest.raises(SystemExit):
        load()


def test_load_exits_when_email_missing(monkeypatch):
    monkeypatch.setenv("TICKET_URL", "https://example.com")
    monkeypatch.setenv("BUYER_NAME", "Test User")
    monkeypatch.delenv("BUYER_EMAIL", raising=False)
    monkeypatch.setenv("BUYER_PASSWORD", "secret")
    with pytest.raises(SystemExit):
        load()


def test_load_exits_when_password_missing(monkeypatch):
    monkeypatch.setenv("TICKET_URL", "https://example.com")
    monkeypatch.setenv("BUYER_NAME", "Test User")
    monkeypatch.setenv("BUYER_EMAIL", "test@example.com")
    monkeypatch.delenv("BUYER_PASSWORD", raising=False)
    with pytest.raises(SystemExit):
        load()
```

- [ ] **Step 2：執行測試確認失敗**

```bash
pytest tests/test_config.py -v
```

Expected: 全部 5 個測試 FAIL，錯誤訊息為 `ModuleNotFoundError`

- [ ] **Step 3：實作 `bot/config.py`**

```python
import os
import sys
from dotenv import load_dotenv


def load() -> dict:
    load_dotenv()
    required = {
        "url": "TICKET_URL",
        "name": "BUYER_NAME",
        "email": "BUYER_EMAIL",
        "password": "BUYER_PASSWORD",
    }
    config = {}
    missing = []
    for key, env_var in required.items():
        value = os.getenv(env_var)
        if not value:
            missing.append(env_var)
        else:
            config[key] = value
    if missing:
        print(f"[錯誤] .env 缺少以下設定：{', '.join(missing)}")
        print("請參考 .env.example 建立 .env 檔案。")
        sys.exit(1)
    return config
```

- [ ] **Step 4：執行測試確認通過**

```bash
pytest tests/test_config.py -v
```

Expected: 全部 5 個測試 PASS

- [ ] **Step 5：Commit**

```bash
git add bot/config.py tests/test_config.py
git commit -m "feat: add config loader with env validation"
```

---

### Task 4：實作 `bot/browser.py`

**Files:**
- Create: `bot/browser.py`

此模組啟動真實 Chrome，不寫單元測試；整合測試於 Task 6 進行。

- [ ] **Step 1：實作 `bot/browser.py`**

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def start() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(options=options)
```

Selenium 4.x 內建 `selenium-manager`，會自動下載對應版本的 chromedriver，無需手動安裝。

- [ ] **Step 2：Commit**

```bash
git add bot/browser.py
git commit -m "feat: add Chrome browser launcher"
```

---

### Task 5：實作 `bot/form.py`（含測試）

**Files:**
- Create: `bot/form.py`
- Create: `tests/test_form.py`

執行此 task 前，確認已從 Task 1 取得三個欄位的 selector。

- [ ] **Step 1：寫失敗的測試**

建立 `tests/test_form.py`：

```python
from unittest.mock import MagicMock, patch
from bot.form import fill


def _make_config():
    return {
        "url": "https://example.com",
        "name": "Test User",
        "email": "test@example.com",
        "password": "secret",
    }


def test_fill_navigates_to_url():
    config = _make_config()
    mock_element = MagicMock()
    with patch("bot.form.WebDriverWait") as mock_wait:
        mock_wait.return_value.until.return_value = mock_element
        driver = MagicMock()
        fill(driver, config)
    driver.get.assert_called_once_with("https://example.com")


def test_fill_clears_and_sends_keys_for_each_field():
    config = _make_config()
    mock_element = MagicMock()
    with patch("bot.form.WebDriverWait") as mock_wait:
        mock_wait.return_value.until.return_value = mock_element
        driver = MagicMock()
        fill(driver, config)
    assert mock_element.clear.call_count == 3
    mock_element.send_keys.assert_any_call("Test User")
    mock_element.send_keys.assert_any_call("test@example.com")
    mock_element.send_keys.assert_any_call("secret")
```

- [ ] **Step 2：執行測試確認失敗**

```bash
pytest tests/test_form.py -v
```

Expected: 全部 2 個測試 FAIL，錯誤訊息為 `ModuleNotFoundError`

- [ ] **Step 3：實作 `bot/form.py`**

將 Task 1 找到的 selector 填入對應常數：

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

WAIT_TIMEOUT = 10

# 將以下三行替換為 Task 1 找到的實際 selector
NAME_SELECTOR = (By.CSS_SELECTOR, "input[name='purchaser_name']")
EMAIL_SELECTOR = (By.CSS_SELECTOR, "input[name='email']")
PASSWORD_SELECTOR = (By.CSS_SELECTOR, "input[name='password']")


def _wait_and_fill(driver, selector: tuple, value: str) -> None:
    element = WebDriverWait(driver, WAIT_TIMEOUT).until(
        EC.visibility_of_element_located(selector)
    )
    element.clear()
    element.send_keys(value)


def fill(driver, config: dict) -> None:
    driver.get(config["url"])
    _wait_and_fill(driver, NAME_SELECTOR, config["name"])
    _wait_and_fill(driver, EMAIL_SELECTOR, config["email"])
    _wait_and_fill(driver, PASSWORD_SELECTOR, config["password"])
```

- [ ] **Step 4：執行測試確認通過**

```bash
pytest tests/test_form.py -v
```

Expected: 全部 2 個測試 PASS

- [ ] **Step 5：Commit**

```bash
git add bot/form.py tests/test_form.py
git commit -m "feat: add form filling logic with explicit waits"
```

---

### Task 6：實作 `main.py` 並執行端對端測試

**Files:**
- Create: `main.py`
- Create: `.env`（本機使用，不提交）

- [ ] **Step 1：實作 `main.py`**

```python
from bot.config import load
from bot import browser, form


def main():
    config = load()
    driver = browser.start()
    try:
        form.fill(driver, config)
        print("\n填寫完成，請在瀏覽器確認後手動送出。")
        input("按 Enter 關閉程式...")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
```

- [ ] **Step 2：建立本機 `.env`**

```bash
cp .env.example .env
```

用文字編輯器開啟 `.env`，填入真實的 BUYER_NAME、BUYER_EMAIL、BUYER_PASSWORD。

- [ ] **Step 3：執行完整測試套件**

```bash
pytest -v
```

Expected: 全部 7 個測試 PASS（5 個 config + 2 個 form）

- [ ] **Step 4：執行端對端測試**

```bash
python main.py
```

Expected 行為：
1. Chrome 視窗開啟
2. 自動導航到購票頁面
3. name / email / password 欄位自動填入
4. 終端機顯示「填寫完成，請在瀏覽器確認後手動送出。」
5. 等待 Enter 鍵後關閉 Chrome

若某個欄位填寫失敗（找不到元素），終端機會顯示 Selenium 的 `TimeoutException`。此時回到 Task 1，重新確認 selector，更新 `bot/form.py` 中對應的常數後重試。

- [ ] **Step 5：Commit**

```bash
git add main.py docs/
git commit -m "feat: wire up main entry point"
```

---

### Task 7：全套測試與最終驗收

- [ ] **Step 1：確認 `.env` 不在 git 追蹤清單內**

```bash
git status
```

Expected：`.env` 不出現在輸出中（被 `.gitignore` 排除）。

- [ ] **Step 2：執行完整測試套件最終確認**

```bash
pytest -v
```

Expected: 全部測試 PASS，無 warning。

- [ ] **Step 3：完成**

專案可以 `python main.py` 正常執行，並準備好進行後續的勾選條款功能擴充（加在 `bot/form.py` 的 `fill()` 末段）與 PyInstaller 打包。
