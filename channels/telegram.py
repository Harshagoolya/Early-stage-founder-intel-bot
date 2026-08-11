import os
import re
import requests
from .base import BaseChannel


class TelegramChannel(BaseChannel):
    """
    Posts to a Telegram channel or group via Bot API.
    Setup: Create a bot via @BotFather, add it to your channel as admin,
    then get the chat_id.
    """

    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id   = os.getenv("TELEGRAM_CHAT_ID")

    def post(self, content: dict) -> bool:
        url  = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

        # Convert markdown to Telegram HTML
        text = content["markdown"]
        text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)

        payload = {
            "chat_id":    self.chat_id,
            "text":       text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }
        try:
            resp = requests.post(url, json=payload, timeout=10)
            if resp.status_code == 200:
                print("[Telegram] ✅ Posted successfully")
                return True
            print(f"[Telegram] ❌ Failed ({resp.status_code}): {resp.text}")
            return False
        except Exception as e:
            print(f"[Telegram] ❌ Exception: {e}")
            return False
