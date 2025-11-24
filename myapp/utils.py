import requests
from django.conf import settings

def send_telegram(text: str) -> bool:
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    try:
        r = requests.post(url, data={"chat_id": chat_id, "text": text})
        return r.ok
    except Exception:
        return False
