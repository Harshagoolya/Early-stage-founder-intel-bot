import os
import requests
from .base import BaseChannel


class EmailChannel(BaseChannel):
    """
    Sends a digest email via Resend (resend.com).
    Free tier: 3,000 emails/month, 100/day.
    """

    def __init__(self):
        self.api_key  = os.getenv("RESEND_API_KEY")
        self.to       = os.getenv("EMAIL_TO")
        self.from_    = os.getenv("EMAIL_FROM", "Founder Intel <digest@yourdomain.com>")

    def post(self, content: dict) -> bool:
        topic    = content["topic"]
        html     = content["html"]
        subject  = f"{topic['emoji']} {topic['name']} — Founder Intel Weekly"

        email_html = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            max-width: 600px; margin: 0 auto; padding: 24px; color: #1a1a1a; }}
    h2   {{ color: #1a1a1a; border-bottom: 2px solid #f0f0f0; padding-bottom: 12px; }}
    h3   {{ color: #1a1a1a; margin-top: 24px; }}
    a    {{ color: #7c3aed; }}
    p    {{ line-height: 1.6; color: #444; }}
    .footer {{ margin-top: 40px; padding-top: 16px; border-top: 1px solid #f0f0f0;
               font-size: 12px; color: #999; }}
  </style>
</head>
<body>
  {html}
  <div class="footer">
    <p>You're receiving this because you subscribed to Founder Intel.<br>
    <a href="https://github.com/Harshagoolya/Early-stage-founder-intel-bot">Open source on GitHub</a></p>
  </div>
</body>
</html>
"""
        payload = {
            "from":    self.from_,
            "to":      [e.strip() for e in self.to.split(",")],
            "subject": subject,
            "html":    email_html,
        }

        try:
            resp = requests.post(
                "https://api.resend.com/emails",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type":  "application/json",
                },
                json=payload,
                timeout=10,
            )
            if resp.status_code in (200, 201):
                print("[Email] ✅ Sent successfully")
                return True
            print(f"[Email] ❌ Failed ({resp.status_code}): {resp.text}")
            return False
        except Exception as e:
            print(f"[Email] ❌ Exception: {e}")
            return False
