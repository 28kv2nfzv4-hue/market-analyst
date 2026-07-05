import os
from datetime import datetime, timezone

import requests

FINNHUB_API_KEY = os.environ["FINNHUB_API_KEY"]
NEWSAPI_API_KEY = os.environ["NEWSAPI_API_KEY"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

CLAUDE_MODEL = "claude-sonnet-5"


def fetch_finnhub_news(limit=10):
    response = requests.get(
        "https://finnhub.io/api/v1/news",
        params={"category": "general", "token": FINNHUB_API_KEY},
        timeout=15,
    )
    response.raise_for_status()
    return [
        {
            "title": article["headline"],
            "summary": article.get("summary", ""),
            "source": article.get("source", "Finnhub"),
            "url": article.get("url", ""),
        }
        for article in response.json()[:limit]
    ]


def fetch_newsapi_news(limit=10):
    response = requests.get(
        "https://newsapi.org/v2/everything",
        params={
            "q": '(geopolitics OR "central bank" OR sanctions OR war OR inflation OR "interest rate" OR tariffs)',
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": limit,
            "apiKey": NEWSAPI_API_KEY,
        },
        timeout=15,
    )
    response.raise_for_status()
    return [
        {
            "title": article["title"],
            "summary": article.get("description") or "",
            "source": article.get("source", {}).get("name", "NewsAPI"),
            "url": article.get("url", ""),
        }
        for article in response.json().get("articles", [])
    ]


def build_prompt(articles):
    headlines = "\n".join(
        f"- [{a['source']}] {a['title']}: {a['summary']} ({a['url']})" for a in articles
    )
    return (
        "You are a financial market analyst. Below are today's financial and "
        "geopolitical news headlines. Write a concise daily market briefing:\n"
        "1. Identify which items are likely to move financial markets (equities, "
        "bonds, currencies, commodities) and explain why.\n"
        "2. Note any significant geopolitical developments and their potential "
        "market impact.\n"
        "3. Keep it tight and actionable — a trader should be able to read this "
        "in under two minutes.\n"
        "Format as plain text suitable for a Telegram message (short paragraphs, "
        "no markdown headers).\n\n"
        f"Today's headlines:\n{headlines}"
    )


def summarize_with_claude(prompt):
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": CLAUDE_MODEL,
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=60,
    )
    response.raise_for_status()
    return response.json()["content"][0]["text"]


TELEGRAM_MAX_MESSAGE_LENGTH = 4096


def send_telegram_message(text):
    text = text[: TELEGRAM_MAX_MESSAGE_LENGTH - 3] + "..." if len(text) > TELEGRAM_MAX_MESSAGE_LENGTH else text

    response = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        json={"chat_id": TELEGRAM_CHAT_ID, "text": text},
        timeout=15,
    )
    if not response.ok:
        print(f"Telegram API error {response.status_code}: {response.text}")
    response.raise_for_status()


def main():
    articles = fetch_finnhub_news() + fetch_newsapi_news()
    if not articles:
        print("No articles fetched; skipping digest.")
        return

    summary = summarize_with_claude(build_prompt(articles))
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    send_telegram_message(f"Market Briefing — {date_str}\n\n{summary}")
    print("Daily digest sent.")


if __name__ == "__main__":
    main()
