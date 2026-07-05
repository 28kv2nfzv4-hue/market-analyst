import os

import requests
from fastapi import APIRouter, Header, HTTPException, Request

router = APIRouter()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_WEBHOOK_SECRET = os.getenv("TELEGRAM_WEBHOOK_SECRET", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = "claude-sonnet-5"

SYSTEM_PROMPT = (
    "You are a financial markets assistant for a personal trading dashboard. "
    "Answer questions about markets, trading strategy, and financial or "
    "geopolitical news concisely and practically. If asked for live prices "
    "or your own trade history, say you don't have live access to that yet."
)


def ask_claude(message: str) -> str:
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
            "system": SYSTEM_PROMPT,
            "messages": [{"role": "user", "content": message}],
        },
        timeout=30,
    )
    response.raise_for_status()
    for block in response.json()["content"]:
        if block.get("type") == "text":
            return block["text"]
    return "Sorry, I couldn't generate a reply."


def send_telegram_message(chat_id: int, text: str) -> None:
    response = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": text},
        timeout=15,
    )
    response.raise_for_status()


@router.post("/telegram/webhook")
async def telegram_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str = Header(default=""),
):
    if TELEGRAM_WEBHOOK_SECRET and x_telegram_bot_api_secret_token != TELEGRAM_WEBHOOK_SECRET:
        raise HTTPException(status_code=403, detail="Invalid secret token")

    update = await request.json()
    message = update.get("message") or {}
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text")

    if chat_id and text:
        reply = ask_claude(text)
        send_telegram_message(chat_id, reply)

    return {"ok": True}
