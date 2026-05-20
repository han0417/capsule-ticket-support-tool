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
