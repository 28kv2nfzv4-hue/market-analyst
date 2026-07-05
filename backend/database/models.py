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

    # Broker-sync fields (nullable — manual trades never set these).
    # NOTE: these columns must be added to any already-deployed database by hand
    # (`ALTER TABLE trades ADD COLUMN ...`) since Base.metadata.create_all only
    # creates missing tables, it never alters an existing one (no Alembic here).
    source = Column(String, nullable=True)  # e.g. "deriv"; null/absent means manual entry
    external_id = Column(String, nullable=True, unique=True)  # dedup key, e.g. deriv contract_id
    exit_price = Column(Float, nullable=True)
    profit_loss = Column(Float, nullable=True)
    opened_at = Column(DateTime, nullable=True)
    closed_at = Column(DateTime, nullable=True)


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
