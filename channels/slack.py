import os
import requests
from .base import BaseChannel


class SlackChannel(BaseChannel):
    """Posts to a Slack channel via incoming webhook."""

    def __init__(self):
        self.webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    def post(self, content: dict) -> bool:
        # Slack uses mrkdwn — convert ** bold to *bold*
        text = content["markdown"].replace("**", "*")

        payload = {
            "text": text,
            "unfurl_links": False,
            "unfurl_media": False,
        }
        try:
            resp = requests.post(self.webhook_url, json=payload, timeout=10)
            if resp.status_code == 200:
                print("[Slack] ✅ Posted successfully")
                return True
            print(f"[Slack] ❌ Failed ({resp.status_code}): {resp.text}")
            return False
        except Exception as e:
            print(f"[Slack] ❌ Exception: {e}")
            return False
