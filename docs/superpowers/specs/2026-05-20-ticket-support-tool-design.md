# 購票輔助工具設計規格

**日期：** 2026-05-20  
**目標網址：** https://www.tbluelinepark.com/ticket_eng/GD2000441  
**技術棧：** Python + Selenium 4.x

---

## 目標

建立一個 Selenium 自動化腳本，開啟 Chrome 瀏覽器，導航到指定購票頁面，自動填寫個人資料欄位與勾選條款，填完後暫停等待使用者手動確認送出。

---

## 架構

```
capsule-ticket-support-tool/
├── main.py              # 入口，協調各模組執行
├── bot/
│   ├── __init__.py
│   ├── browser.py       # Chrome WebDriver 啟動設定
│   ├── form.py          # 表單填寫邏輯（欄位填寫、條款勾選）
│   └── config.py        # 讀取 .env，驗證必填欄位
├── .env                 # 實際設定值（gitignore）
├── .env.example         # 設定範本
├── requirements.txt
└── docs/
    └── superpowers/
        └── specs/
            └── 2026-05-20-ticket-support-tool-design.md
```

---

## 模組職責

### `bot/config.py`
- 使用 `python-dotenv` 載入 `.env`
- 驗證 `TICKET_URL`、`BUYER_NAME`、`BUYER_EMAIL`、`BUYER_PASSWORD` 均存在
- 缺少任何欄位時立刻拋出明確錯誤訊息
- 回傳包含三個欄位的 dict

### `bot/browser.py`
- 使用 Selenium 4.x（內建 `selenium-manager`，自動管理 chromedriver，不需手動安裝）
- 啟動可見的 Chrome 視窗（非 headless）
- 回傳 `webdriver.Chrome` 實例

### `bot/form.py`
- 接收 `driver` 與 `config` dict
- 導航到目標網址
- 使用 `WebDriverWait`（顯式等待，最多 10 秒）等待每個欄位出現後再操作
- 依序填寫：`name` → `email` → `password`
- 填完後 print 提示訊息，腳本暫停（`input()` 等待使用者按 Enter 關閉）
- 各欄位的 CSS selector / XPath 集中定義在模組頂部常數，方便日後維護

### `main.py`
- 依序呼叫 `config.load()` → `browser.start()` → `form.fill()`
- 捕捉例外，print 友善錯誤訊息

---

## 設定檔

**.env.example（範本，提交到 git）：**
```
TICKET_URL=https://www.tbluelinepark.com/ticket_eng/GD2000441
BUYER_NAME=王小明
BUYER_EMAIL=your_email@example.com
BUYER_PASSWORD=your_password_here
```

**.env（實際值，加入 .gitignore）：**
使用者複製 `.env.example` 為 `.env` 並填入真實資料。

---

## 執行流程

1. 使用者複製 `.env.example` → `.env`，填入個人資料
2. 執行 `python main.py`
3. Chrome 自動開啟，導航到購票頁面
4. 欄位依序自動填入
5. 終端機顯示「已填完，請在瀏覽器確認後手動送出，按 Enter 結束程式」
6. 使用者在瀏覽器手動按送出後，回到終端機按 Enter 結束

---

## 依賴套件

```
selenium>=4.0.0
python-dotenv>=1.0.0
```

---

## 打包方案（後期）

- 工具：`PyInstaller`
- 目標平台：macOS
- 指令：`pyinstaller --onefile main.py`
- 使用者須自行安裝 Chrome（工具不內含瀏覽器）
- `.env` 需與執行檔放在同一目錄下

---

## 範圍外（本次不實作）

- 條款勾選邏輯（另行討論後加入 `form.py`）
- Windows / 跨平台打包
- 重試 / 定時輪詢機制
- GUI 介面
