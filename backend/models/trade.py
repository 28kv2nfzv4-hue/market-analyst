from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class TradeDirection(str, Enum):
	BUY = "buy"
	SELL = "sell"


class TradeResult(str, Enum):
	WIN = "win"
	LOSS = "loss"
	BREAKEVEN = "breakeven"
	PENDING = "pending"


class Trade(BaseModel):
	pair: str = Field(..., example="EURUSD")
	direction: TradeDirection
	entry_price: float
	stop_loss: float
	take_profit: float
	risk_percent: float = Field(..., ge=0, le=100)
	result: TradeResult = TradeResult.PENDING
	notes: Optional[str] = None

	# Broker-sync fields — unset for manually-entered trades.
	source: Optional[str] = None
	external_id: Optional[str] = None
	exit_price: Optional[float] = None
	profit_loss: Optional[float] = None
	opened_at: Optional[datetime] = None
	closed_at: Optional[datetime] = None


class TradeOut(Trade):
	model_config = {"from_attributes": True}

	id: int


class TradeUpdate(BaseModel):
	pair: Optional[str] = None
	direction: Optional[TradeDirection] = None
	entry_price: Optional[float] = None
	stop_loss: Optional[float] = None
	take_profit: Optional[float] = None
	risk_percent: Optional[float] = Field(default=None, ge=0, le=100)
	result: Optional[TradeResult] = None
	notes: Optional[str] = None
