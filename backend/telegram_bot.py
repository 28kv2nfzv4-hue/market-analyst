import os
from typing import Optional

import requests
from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import ChatMessageORM, DigestORM, TradeORM

router = APIRouter()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_WEBHOOK_SECRET = os.getenv("TELEGRAM_WEBHOOK_SECRET", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = "claude-sonnet-5"

HISTORY_LIMIT = 10  # messages kept per chat for conversation context
TELEGRAM_MAX_LEN = 4096

WELCOME_MESSAGE = (
    "Welcome! I'm your trading dashboard assistant. Ask me about your trades, "
    "the latest market digest, or anything markets-related."
)

SYSTEM_PROMPT_TEMPLATE = (
    "You are a financial markets assistant for a personal trading dashboard. "
    "Answer questions about markets, trading strategy, and financial or "
    "geopolitical news concisely and practically.\n\n"
    "The user's current trade log summary:\n{trade_summary}\n\n"
    "The most recent daily market digest you sent them:\n{latest_digest}"
)


def build_trade_summary(db: Session) -> str:
    trades = db.query(TradeORM).all()
    if not trades:
        return "No trades logged yet."

    wins = sum(1 for t in trades if t.result == "win")
    losses = sum(1 for t in trades if t.result == "loss")
    pending = sum(1 for t in trades if t.result == "pending")
    recent_lines = "\n".join(
        f"- {t.pair} {t.direction} @ {t.entry_price} -> {t.result}" for t in trades[-5:]
    )
    return (
        f"Total: {len(trades)}, Wins: {wins}, Losses: {losses}, Pending: {pending}\n"
        f"Most recent trades:\n{recent_lines}"
    )


def build_latest_digest(db: Session) -> str:
    digest = db.query(DigestORM).order_by(DigestORM.id.desc()).first()
    return digest.content if digest else "No digest sent yet."


def get_recent_history(db: Session, chat_id: str):
    messages = (
        db.query(ChatMessageORM)
        .filter(ChatMessageORM.chat_id == chat_id)
        .order_by(ChatMessageORM.id.desc())
        .limit(HISTORY_LIMIT)
        .all()
    )
    return list(reversed(messages))


def ask_claude(db: Session, chat_id: str, message: str) -> str:
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
        trade_summary=build_trade_summary(db),
        latest_digest=build_latest_digest(db),
    )

    history = get_recent_history(db, chat_id)
    messages = [{"role": m.role, "content": m.content} for m in history]
    messages.append({"role": "user", "content": message})

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
            "system": system_prompt,
            "messages": messages,
        },
        timeout=30,
    )
    response.raise_for_status()
    for block in response.json()["content"]:
        if block.get("type") == "text":
            return block["text"]
    return "Sorry, I couldn't generate a reply."


def send_telegram_message(chat_id: int, text: str) -> None:
    if len(text) > TELEGRAM_MAX_LEN:
        text = text[: TELEGRAM_MAX_LEN - 3] + "..."

    response = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": text},
        timeout=15,
    )
    response.raise_for_status()


def parse_start_command(text: str) -> Optional[str]:
    parts = text.strip().split(maxsplit=1)
    if parts and parts[0] == "/start":
        return parts[1] if len(parts) > 1 else ""
    return None


@router.post("/telegram/webhook")
async def telegram_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str = Header(default=""),
    db: Session = Depends(get_db),
):
    if TELEGRAM_WEBHOOK_SECRET and x_telegram_bot_api_secret_token != TELEGRAM_WEBHOOK_SECRET:
        raise HTTPException(status_code=403, detail="Invalid secret token")

    update = await request.json()
    message = update.get("message") or {}
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text")

    if chat_id and text:
        chat_id_str = str(chat_id)

        start_payload = parse_start_command(text)
        if start_payload is not None:
            send_telegram_message(chat_id, WELCOME_MESSAGE)
            return {"ok": True}

        db.add(ChatMessageORM(chat_id=chat_id_str, role="user", content=text))
        db.commit()

        reply = ask_claude(db, chat_id_str, text)

        db.add(ChatMessageORM(chat_id=chat_id_str, role="assistant", content=reply))
        db.commit()

        send_telegram_message(chat_id, reply)

    return {"ok": True}
