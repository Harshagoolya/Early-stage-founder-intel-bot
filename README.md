README (1)
🤖 Founder Intel
An open-source AI agent that delivers curated, tactical articles on Growth & Scaling, Fundraising, and Product Monetization to early-stage founders — twice a week, on any platform you choose.
What it does
Every Tuesday and Friday, Founder Intel:
Researches the web for fresh articles (last 45 days) using Tavily
Filters them with Claude — only articles scoring 4/5+ for seed/Series A relevance get through
Writes a tactical digest tailored for early-stage founders
Delivers it to any channel you configure
No generic advice. No enterprise fluff. Just what matters at the seed and Series A stage.
Supported channels
Channel
Setup difficulty
Best for
Discord
⭐ Easy
Communities, founder groups
Slack
⭐ Easy
Team workspaces
Email
⭐⭐ Medium
Newsletters, personal digest
Telegram
⭐⭐ Medium
International communities
You can enable any combination — just add the relevant env vars.
Quick start
1. Fork this repo
Click Fork at the top right of this page.
2. Get your API keys
Key
Where
Free tier?
ANTHROPIC_API_KEY
console.anthropic.com
Pay-per-use (~$0.28/mo for this use case)
TAVILY_API_KEY
tavily.com
✅ 1,000 searches/month
3. Set up your channel(s)
<details>
<summary><b>Discord</b></summary>
Open your Discord server
Go to Server Settings → Integrations → Webhooks → New Webhook
Choose your channel, copy the webhook URL
Add as DISCORD_WEBHOOK_URL in your secrets
</details>
<details>
<summary><b>Slack</b></summary>
Go to api.slack.com/apps → Create New App → From Scratch
Go to Incoming Webhooks → Activate → Add New Webhook to Workspace
Choose your channel, copy the webhook URL
Add as SLACK_WEBHOOK_URL in your secrets
</details>
<details>
<summary><b>Email (via Resend)</b></summary>
Sign up at resend.com (free: 3,000 emails/month)
Add and verify your sending domain
Create an API key
Add RESEND_API_KEY, EMAIL_FROM, and EMAIL_TO to your secrets
</details>
<details>
<summary><b>Telegram</b></summary>
Message @BotFather on Telegram → /newbot
Copy the bot token
Add your bot to your channel as an admin
Get your chat ID by messaging @userinfobot
Add TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID to your secrets
</details>
4. Add GitHub secrets
Go to your repo → Settings → Secrets and variables → Actions and add:
ANTHROPIC_API_KEY      (required)
TAVILY_API_KEY         (required)
DISCORD_WEBHOOK_URL    (if using Discord)
SLACK_WEBHOOK_URL      (if using Slack)
RESEND_API_KEY         (if using Email)
EMAIL_FROM             (if using Email)
EMAIL_TO               (if using Email)
TELEGRAM_BOT_TOKEN     (if using Telegram)
TELEGRAM_CHAT_ID       (if using Telegram)
​
5. Test it
Go to Actions → Founder Intel Agent → Run workflow → Run workflow
Customization
Change the schedule
Edit the cron expressions in .github/workflows/agent.yml:
- cron: "0 9 * * 2"   # Tuesday 09:00 UTC
- cron: "0 9 * * 5"   # Friday 09:00 UTC
​
Use crontab.guru to build your own schedule.
Add a topic
Add an entry to the TOPICS list in agent.py:
{
    "name": "Hiring & Team Building",
    "emoji": "👥",
    "search_queries": [
        "early stage startup hiring tactics seed stage 2025",
        "first 10 hires startup founder advice",
    ],
},
​
Add a new channel
Create channels/yourchannel.py
Subclass BaseChannel and implement post(content: dict) -> bool
Import and add it to load_channels() in agent.py
The content dict has three formats:
content["markdown"] — for Discord/Slack
content["plain"] — for Telegram/SMS
content["html"] — for email
Cost
Running twice a week costs roughly $0.28/month in Claude API fees. Tavily's free tier (1,000 credits/month) covers all searches. GitHub Actions is free.
Service
Monthly cost
Anthropic (Claude Sonnet)
~$0.28
Tavily
Free
GitHub Actions
Free
Total
~$0.28
Project structure
founder-intel/
├── agent.py                  # Main agent logic
├── channels/
│   ├── base.py               # Abstract base class
│   ├── discord.py            # Discord webhook
│   ├── slack.py              # Slack webhook
│   ├── email.py              # Email via Resend
│   └── telegram.py           # Telegram bot
├── requirements.txt
├── .env.example
└── .github/
    └── workflows/
        └── agent.yml         # GitHub Actions schedule
​
Contributing
PRs welcome! Ideas for contributions:
New channels (WhatsApp, Linear, Notion, MS Teams, SMS)
New topic categories
Web UI for non-technical users
Analytics/tracking of most-clicked articles
Please open an issue before starting large features.
License
MIT — use it, fork it, build on it.
Built for founders, by founders. If this helps you, give it a ⭐
