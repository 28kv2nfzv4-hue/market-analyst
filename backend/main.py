import os
from typing import List

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database.database import Base, engine, get_db
from database.models import DigestORM, TradeORM
from models.digest import DigestIn, DigestOut
from models.trade import Trade, TradeOut
from telegram_bot import router as telegram_router

DIGEST_API_SECRET = os.getenv("DIGEST_API_SECRET", "")


def verify_digest_secret(x_digest_secret: str = Header(default="")):
    if DIGEST_API_SECRET and x_digest_secret != DIGEST_API_SECRET:
        raise HTTPException(status_code=403, detail="Invalid secret")

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Project Atlas API", version="0.1.0")
app.include_router(telegram_router)

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


@app.post("/digests", dependencies=[Depends(verify_digest_secret)])
def create_digest(digest: DigestIn, db: Session = Depends(get_db)):
    db_digest = DigestORM(content=digest.content)
    db.add(db_digest)
    db.commit()
    db.refresh(db_digest)
    return {"id": db_digest.id}


@app.get("/digests", response_model=List[DigestOut])
def list_digests(db: Session = Depends(get_db)):
    return db.query(DigestORM).order_by(DigestORM.id.desc()).limit(30).all()