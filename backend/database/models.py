from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Enum as SAEnum, Float, Integer, String

from database.database import Base
from models.trade import TradeDirection, TradeResult


class TradeORM(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    pair = Column(String, nullable=False)
    direction = Column(SAEnum(TradeDirection), nullable=False)
    entry_price = Column(Float, nullable=False)
    stop_loss = Column(Float, nullable=False)
    take_profit = Column(Float, nullable=False)
    risk_percent = Column(Float, nullable=False)
    result = Column(SAEnum(TradeResult), nullable=False, default=TradeResult.PENDING)
    notes = Column(String, nullable=True)


class ChatMessageORM(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String, nullable=False, index=True)
    role = Column(String, nullable=False)  # "user" or "assistant"
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class DigestORM(Base):
    __tablename__ = "digests"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
