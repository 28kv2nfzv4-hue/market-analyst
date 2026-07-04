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


class TradeOut(Trade):
	model_config = {"from_attributes": True}

	id: int
