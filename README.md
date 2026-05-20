# Capsule Ticket Support Tool

自動操作 [海雲台藍線樂園](https://www.tbluelinepark.com) 購票頁面的輔助工具。執行後會自動開啟 Chrome、填好所有欄位、勾好條款、切換到下個月並點選指定日期，最後等待你手動按下確認送出。

---

## 事前準備

### 1. 安裝 Python

需要 Python 3.9 以上版本。確認方式：

```bash
python3 --version
```

### 2. 安裝 Google Chrome

確認電腦上已安裝 Chrome 瀏覽器。工具會自動下載對應版本的 ChromeDriver，**不需要手動安裝**。

### 3. 安裝依賴套件

```bash
pip3 install -r requirements.txt
```

---

## 使用方式

### Step 1：建立設定檔

複製範本並填入你的個人資料：

```bash
cp .env.example .env
```

用任何文字編輯器開啟 `.env`，填入以下欄位：

```
TICKET_URL=https://www.tbluelinepark.com/ticket_eng/GD2000441
BUYER_NAME=你的英文姓名
BUYER_EMAIL=你的電子信箱
BUYER_PASSWORD=1234
TICKET_DAY=21
```

| 欄位 | 說明 |
|------|------|
| `TICKET_URL` | 購票頁面網址 |
| `BUYER_NAME` | 購票人英文姓名 |
| `BUYER_EMAIL` | 購票人電子信箱 |
| `BUYER_PASSWORD` | 4 位數查詢 PIN（非登入密碼） |
| `TICKET_DAY` | 欲購買的日期（幾號），預設 `21` |

> **注意：`BUYER_PASSWORD` 只填 4 位數字。** 這是網站用來之後查詢訂單的 4 位 PIN，不是你的登入密碼。

### Step 2：執行工具

```bash
python3 main.py
```

### Step 3：手動送出

工具會自動完成以下動作：

1. 開啟 Chrome 並導航到購票頁面
2. 填入姓名、Email、密碼（4 位 PIN）
3. 選擇國籍（Taiwan）
4. 勾選所有必要條款
5. 切換到下個月，點選 `.env` 中 `TICKET_DAY` 指定的日期

全部完成後，終端機會顯示：

```
填寫完成，請在瀏覽器確認後手動送出。
按 Enter 關閉程式...
```

此時在瀏覽器確認資料無誤，按下購票按鈕送出。回到終端機按 Enter 關閉 Chrome。

---

## 常見問題

### 頁面載入很慢、工具提早噴錯

購票當天伺服器可能壅塞，網頁可能需要數分鐘才載完。預設的等待時間如下，可依需求調整：

開啟 `bot/form.py`，找到最上方的三個常數：

```python
# 等待整個頁面載入完成（秒）
PAGE_LOAD_TIMEOUT = 300   # ← 調這個（目前 5 分鐘）

# 等待頁面上的欄位可互動（秒）
ELEMENT_TIMEOUT = 30      # ← 調這個（適用姓名、Email 等靜態欄位）

# 等待 AJAX 動態載入的內容出現（秒）
AJAX_TIMEOUT = 60         # ← 調這個（適用日期 live 狀態、時段選單）
```

### 點選日期後跳出「This schedule has been sold out」

表示該日期已售完，工具會自動 dismiss 彈窗並拋出錯誤。請確認 `.env` 中的 `TICKET_DAY` 對應的日期確實有開放購票。

### `.env` 檔案遺失或格式錯誤

執行時若看到 `[錯誤] .env 缺少以下設定`，請確認 `.env` 存在且四個欄位都有填值。可參考 `.env.example` 的格式重新建立。

### 某個欄位沒有填到

若程式執行完但欄位是空的，代表網站的 HTML 結構可能有改動。請使用 Chrome DevTools（F12）重新確認各欄位的 `id`，並更新 `bot/form.py` 對應的 Selector 常數。

---

## 專案結構

```
capsule-ticket-support-tool/
├── main.py          # 入口：執行這個
├── bot/
│   ├── config.py    # 讀取 .env 設定
│   ├── browser.py   # 啟動 Chrome
│   └── form.py      # 表單填寫邏輯（Selector 和 Timeout 都在這）
├── .env             # 你的個人設定（不上傳 git）
├── .env.example     # 設定範本
└── requirements.txt # 依賴套件
```

---

## 執行測試

```bash
python3 -m pytest -v
```
