import os
import requests
from .base import BaseChannel


class DiscordChannel(BaseChannel):
    """Posts to a Discord channel via webhook."""

    def __init__(self):
        self.webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    def post(self, content: dict) -> bool:
        payload = {
            "content": content["markdown"],
            "username": "Founder Intel",
            "avatar_url": "https://cdn.discordapp.com/embed/avatars/0.png",
        }
        try:
            resp = requests.post(self.webhook_url, json=payload, timeout=10)
            if resp.status_code in (200, 204):
                print("[Discord] ✅ Posted successfully")
                return True
            print(f"[Discord] ❌ Failed ({resp.status_code}): {resp.text}")
            return False
        except Exception as e:
            print(f"[Discord] ❌ Exception: {e}")
            return False
