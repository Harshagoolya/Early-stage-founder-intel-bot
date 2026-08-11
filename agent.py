"""
Founder Intel Agent
====================
Researches and posts curated articles on Growth & Scaling, Fundraising,
and Product Monetization for seed/Series A founders — to any channel you configure.

Supported channels: Discord, Slack, Email, Telegram
"""

import os
import json
import time
import schedule
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import anthropic
from tavily import TavilyClient

from channels.discord  import DiscordChannel
from channels.slack    import SlackChannel
from channels.email    import EmailChannel
from channels.telegram import TelegramChannel

load_dotenv()

# ── Topics ─────────────────────────────────────────────────────────────────────

TOPICS = [
    {
        "name": "Growth & Scaling",
        "emoji": "📈",
        "search_queries": [
            "early stage startup growth tactics seed series A 2025",
            "B2B SaaS growth hacks founder playbook 2025",
            "consumer app user acquisition strategy seed stage",
        ],
    },
    {
        "name": "Fundraising",
        "emoji": "💰",
        "search_queries": [
            "seed series A fundraising tips founders 2025",
            "venture capital pitch deck advice early stage 2025",
            "startup fundraising mistakes seed stage founders",
        ],
    },
    {
        "name": "Product Monetization",
        "emoji": "🚀",
        "search_queries": [
            "consumer tech monetization strategy early stage startup 2025",
            "SaaS pricing model seed series A founders",
            "product led growth monetization consumer app 2025",
        ],
    },
]

STATE_FILE = Path("agent_state.json")

# ── Channel loader ──────────────────────────────────────────────────────────────

def load_channels() -> list:
    """
    Load all enabled channels from environment variables.
    Add or remove channels here to enable/disable them.
    """
    channels = []

    if os.getenv("DISCORD_WEBHOOK_URL"):
        channels.append(DiscordChannel())

    if os.getenv("SLACK_WEBHOOK_URL"):
        channels.append(SlackChannel())

    if os.getenv("EMAIL_TO") and os.getenv("RESEND_API_KEY"):
        channels.append(EmailChannel())

    if os.getenv("TELEGRAM_BOT_TOKEN") and os.getenv("TELEGRAM_CHAT_ID"):
        channels.append(TelegramChannel())

    return channels

# ── State ───────────────────────────────────────────────────────────────────────

def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"topic_index": 0, "posted_urls": [], "run_count": 0}


def save_state(state: dict):
    STATE_FILE.write_text(json.dumps(state, indent=2))

# ── Research ────────────────────────────────────────────────────────────────────

def research_articles(topic: dict, max_results: int = 5) -> list[dict]:
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    articles = []
    seen_urls = set()

    for query in topic["search_queries"]:
        try:
            response = client.search(
                query=query,
                search_depth="advanced",
                max_results=max_results,
                include_answer=False,
                include_raw_content=False,
                days=45,
            )
            for result in response.get("results", []):
                url = result.get("url", "")
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    articles.append({
                        "title":   result.get("title", "Untitled"),
                        "url":     url,
                        "content": result.get("content", ""),
                        "score":   result.get("score", 0),
                    })
        except Exception as e:
            print(f"[Research] Error for query '{query}': {e}")

    articles.sort(key=lambda x: x["score"], reverse=True)
    return articles[:6]

# ── Quality gate ────────────────────────────────────────────────────────────────

def filter_articles(articles: list[dict], topic: dict, posted_urls: list[str]) -> list[dict]:
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    filtered = []

    for article in articles:
        if article["url"] in posted_urls:
            continue

        prompt = f"""
Rate this article's relevance for early-stage seed/Series A startup founders on the topic of "{topic['name']}".

Title: {article['title']}
Excerpt: {article['content'][:500]}

Score 1–5 where:
5 = Highly actionable, specific to early-stage/seed/Series A
4 = Useful for founders at this stage
3 = Somewhat relevant but generic
2 = Too advanced (Series B+) or not startup-focused
1 = Not relevant

Reply with ONLY a JSON object: {{"score": <number>, "reason": "<one sentence>"}}
"""
        try:
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=100,
                messages=[{"role": "user", "content": prompt}],
            )
            result = json.loads(response.content[0].text.strip())
            article["relevance_score"] = result.get("score", 0)
            article["relevance_reason"] = result.get("reason", "")
            if article["relevance_score"] >= 4:
                filtered.append(article)
        except Exception as e:
            print(f"[Filter] Error scoring '{article['title']}': {e}")

    filtered.sort(key=lambda x: x["relevance_score"], reverse=True)
    return filtered[:3]

# ── Content generation ──────────────────────────────────────────────────────────

def generate_content(articles: list[dict], topic: dict) -> dict:
    """
    Generate content in multiple formats for different channels.
    Returns a dict with 'markdown', 'plain', and 'html' versions.
    """
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    articles_text = "\n\n".join(
        f"Title: {a['title']}\nURL: {a['url']}\nExcerpt: {a['content'][:600]}"
        for a in articles
    )

    prompt = f"""
You are a curator writing for early-stage seed and Series A startup founders building consumer tech.

Topic: {topic['name']}

Articles:
{articles_text}

Write a digest in THREE formats. Separate each with ---FORMAT---.

FORMAT 1 - MARKDOWN (for Discord/Slack, use ** for bold, [text](url) for links):
{topic['emoji']} **{topic['name']} — Weekly Digest**
*For seed & Series A founders building consumer tech*

[For each article:]
**[title](url)**
2-3 tactical sentences on why this matters for seed/Series A founders.

🔑 This week's theme: [one sentence tying articles together]

---FORMAT---

FORMAT 2 - PLAIN TEXT (for Telegram, no markdown):
{topic['emoji']} {topic['name']} — Weekly Digest
For seed & Series A founders building consumer tech

[For each article:]
TITLE: [title]
LINK: [url]
2-3 tactical sentences on why this matters for seed/Series A founders.

Key theme: [one sentence]

---FORMAT---

FORMAT 3 - HTML (for email):
<h2>{topic['emoji']} {topic['name']} — Weekly Digest</h2>
<p><em>For seed & Series A founders building consumer tech</em></p>

[For each article:]
<h3><a href="url">title</a></h3>
<p>2-3 tactical sentences on why this matters for seed/Series A founders.</p>

<p><strong>🔑 This week's theme:</strong> [one sentence]</p>

Rules: Be concrete and tactical. No generic advice. Under 60 words per article summary.
"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        system="You write sharp, tactical content for startup founders. No fluff.",
        messages=[{"role": "user", "content": prompt}],
    )

    parts = response.content[0].text.strip().split("---FORMAT---")
    return {
        "markdown": parts[0].strip() if len(parts) > 0 else "",
        "plain":    parts[1].strip() if len(parts) > 1 else "",
        "html":     parts[2].strip() if len(parts) > 2 else "",
        "topic":    topic,
        "articles": articles,
    }

# ── Main run ────────────────────────────────────────────────────────────────────

def run_agent():
    print(f"\n[Agent] Run started at {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    channels = load_channels()
    if not channels:
        print("[Agent] No channels configured. Add at least one to your .env file.")
        return

    print(f"[Agent] Channels active: {[c.__class__.__name__ for c in channels]}")

    state  = load_state()
    topic  = TOPICS[state["topic_index"] % len(TOPICS)]
    print(f"[Agent] Topic: {topic['name']}")

    print("[Agent] Researching articles...")
    articles = research_articles(topic)
    print(f"[Agent] Found {len(articles)} raw articles")

    if not articles:
        print("[Agent] No articles found. Skipping.")
        return

    print("[Agent] Filtering for relevance...")
    good_articles = filter_articles(articles, topic, state["posted_urls"])
    print(f"[Agent] {len(good_articles)} articles passed quality gate")

    if not good_articles:
        print("[Agent] No articles passed quality gate. Skipping.")
        return

    print("[Agent] Generating content...")
    content = generate_content(good_articles, topic)

    any_success = False
    for channel in channels:
        success = channel.post(content)
        if success:
            any_success = True

    if any_success:
        state["posted_urls"].extend([a["url"] for a in good_articles])
        state["posted_urls"] = state["posted_urls"][-100:]
        state["topic_index"] = (state["topic_index"] + 1) % len(TOPICS)
        state["run_count"] += 1
        save_state(state)
        print(f"[Agent] ✅ Done. Total runs: {state['run_count']}")
    else:
        print("[Agent] ❌ All channels failed. State not updated.")


def main():
    print("🤖 Founder Intel Agent started")
    print("📅 Schedule: Tuesday and Friday at 09:00")

    schedule.every().tuesday.at("09:00").do(run_agent)
    schedule.every().friday.at("09:00").do(run_agent)

    # Uncomment to test immediately:
    # run_agent()

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()
