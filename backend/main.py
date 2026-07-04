import os
from typing import List

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database.database import Base, engine, get_db
from database.models import TradeORM
from models.trade import Trade, TradeOut

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Project Atlas API", version="0.1.0")

allow_origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
allow_origins += [
    origin.strip() for origin in os.getenv("CORS_ORIGINS", "").split(",") if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Welcome to Project Atlas 🚀",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/version")
def version():
    return {
        "version": app.version
    }
@app.post("/trades", response_model=TradeOut)
def create_trade(trade: Trade, db: Session = Depends(get_db)):
    db_trade = TradeORM(**trade.model_dump())
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    return db_trade


@app.get("/trades", response_model=List[TradeOut])
def list_trades(db: Session = Depends(get_db)):
    return db.query(TradeORM).all()