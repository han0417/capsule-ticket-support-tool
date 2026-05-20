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

    raw_day = os.getenv("TICKET_DAY", "21")
    try:
        config["day"] = int(raw_day)
    except ValueError:
        print(f"[錯誤] TICKET_DAY 必須是數字，目前值為：{raw_day}")
        sys.exit(1)

    return config
