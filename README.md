# Founder Intel

An open-source AI agent that delivers curated articles on Growth & Scaling, Fundraising, and Product Monetization to early-stage founders — twice a week, on any platform you choose.

## What it does

Every Tuesday and Friday, Founder Intel:

1. Searches the web for fresh articles (last 45 days) using Tavily
2. Filters them with Claude — only articles scoring 4/5+ for seed/Series A founders get through
3. Writes a tactical digest, no fluff
4. Posts it to whatever channel you configure

## Supported channels

| Channel | Setup | Best for |
|---------|-------|----------|
| Discord | Easy | Communities, founder groups |
| Slack | Easy | Team workspaces |
| Email | Medium | Newsletters, personal digest |
| Telegram | Medium | International communities |

Mix and match — enable any combination by adding the relevant env vars.

## Quick start

### 1. Fork this repo

Click Fork at the top right.

### 2. Get your API keys

- **Anthropic** — console.anthropic.com (pay per use, ~$0.28/month for this)
- **Tavily** — tavily.com (free tier: 1,000 searches/month)

### 3. Set up a channel

**Discord**
- Server Settings > Integrations > Webhooks > New Webhook
- Copy the URL, add as `DISCORD_WEBHOOK_URL`

**Slack**
- api.slack.com/apps > Create App > Incoming Webhooks
- Copy the URL, add as `SLACK_WEBHOOK_URL`

**Email (via Resend)**
- Sign up at resend.com (free: 3,000 emails/month)
- Add `RESEND_API_KEY`, `EMAIL_FROM`, `EMAIL_TO`

**Telegram**
- Create a bot via @BotFather, add it to your channel as admin
- Add `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`

### 4. Add GitHub secrets

Go to Settings > Secrets and variables > Actions and add whichever apply:
ANTHROPIC_API_KEY
TAVILY_API_KEY
DISCORD_WEBHOOK_URL
SLACK_WEBHOOK_URL
RESEND_API_KEY
EMAIL_FROM
EMAIL_TO
TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID

### 5. Test it

Actions > Founder Intel Agent > Run workflow

## Customization

**Change the schedule** — edit the cron lines in `.github/workflows/agent.yml`

**Add a topic** — add an entry to the `TOPICS` list in `agent.py` with a name, emoji, and search queries

**Add a new channel** — create `channels/yourchannel.py`, subclass `BaseChannel`, implement `post()`, and add it to `load_channels()` in `agent.py`

## Cost

About $0.28/month total. Tavily and GitHub Actions are free.

## Contributing

PRs welcome. Good places to start:
- New channels (WhatsApp, Notion, MS Teams)
- New topic categories
- Web UI for non-technical users

Please open an issue before starting anything large.

## License

MIT. Use it, fork it, build on it.

---

Built for founders, by founders. If this helps you, give it a star.

