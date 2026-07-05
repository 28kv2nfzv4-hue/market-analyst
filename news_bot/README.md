# Daily Market Digest

Fetches financial market news (Finnhub) and geopolitical/economic news (NewsAPI), asks Claude to summarize likely market impact, and pushes the result to Telegram. Runs daily via `.github/workflows/daily-digest.yml` (weekdays, 12:00 UTC by default).

## Required credentials

| Variable | Where to get it |
|---|---|
| `FINNHUB_API_KEY` | [finnhub.io/register](https://finnhub.io/register) — free tier |
| `NEWSAPI_API_KEY` | [newsapi.org/register](https://newsapi.org/register) — free tier |
| `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com) — requires billing set up |
| `TELEGRAM_BOT_TOKEN` | Message [@BotFather](https://t.me/BotFather) on Telegram, `/newbot`, follow prompts |
| `TELEGRAM_CHAT_ID` | Message your new bot once, then visit `https://api.telegram.org/bot<TOKEN>/getUpdates` and read `message.chat.id` from the response |

## Optional configuration

| Variable | Purpose |
|---|---|
| `BACKEND_API_URL` | Base URL of the backend API; if set, the digest is also stored via `POST /digests` so it shows up on the dashboard's digest history page |
| `DIGEST_API_SECRET` | Must match the backend's `DIGEST_API_SECRET` env var; leave unset if the backend has none configured |
| `FINNHUB_LIMIT` | Number of Finnhub articles to fetch (default `10`) |
| `NEWSAPI_LIMIT` | Number of NewsAPI articles to fetch (default `10`) |

## Set as GitHub Actions secrets

Run these yourself (so the values never pass through any AI session):

```bash
gh secret set FINNHUB_API_KEY
gh secret set NEWSAPI_API_KEY
gh secret set ANTHROPIC_API_KEY
gh secret set TELEGRAM_BOT_TOKEN
gh secret set TELEGRAM_CHAT_ID
```

Each prompts for the value interactively.

## Test locally

```bash
cd news_bot
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in real values
set -a && source .env && set +a
python digest.py
```

## Test the scheduled workflow without waiting for the cron

```bash
gh workflow run daily-digest.yml
```
