import os
from typing import List

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database.database import Base, engine, get_db
from database.models import DigestORM, TradeORM
from models.digest import DigestIn, DigestOut
from models.trade import Trade, TradeOut, TradeUpdate
from telegram_bot import router as telegram_router

DIGEST_API_SECRET = os.getenv("DIGEST_API_SECRET", "")
BROKER_SYNC_SECRET = os.getenv("BROKER_SYNC_SECRET", "")


def verify_digest_secret(x_digest_secret: str = Header(default="")):
    if DIGEST_API_SECRET and x_digest_secret != DIGEST_API_SECRET:
        raise HTTPException(status_code=403, detail="Invalid secret")


def verify_broker_sync_secret(x_broker_sync_secret: str = Header(default="")):
    if BROKER_SYNC_SECRET and x_broker_sync_secret != BROKER_SYNC_SECRET:
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


@app.patch("/trades/{trade_id}", response_model=TradeOut)
def update_trade(trade_id: int, payload: TradeUpdate, db: Session = Depends(get_db)):
    db_trade = db.query(TradeORM).filter(TradeORM.id == trade_id).first()
    if not db_trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(db_trade, field, value)
    db.commit()
    db.refresh(db_trade)
    return db_trade


@app.delete("/trades/{trade_id}")
def delete_trade(trade_id: int, db: Session = Depends(get_db)):
    db_trade = db.query(TradeORM).filter(TradeORM.id == trade_id).first()
    if not db_trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    db.delete(db_trade)
    db.commit()
    return {"deleted": trade_id}


@app.post(
    "/trades/sync",
    response_model=List[TradeOut],
    dependencies=[Depends(verify_broker_sync_secret)],
)
def sync_broker_trades(trades: List[Trade], db: Session = Depends(get_db)):
    created = []
    for t in trades:
        if t.external_id and db.query(TradeORM).filter(TradeORM.external_id == t.external_id).first():
            continue  # closed broker contracts are immutable, skip-if-exists is enough
        db_trade = TradeORM(**t.model_dump())
        db.add(db_trade)
        db.flush()
        created.append(db_trade)
    db.commit()
    for trade in created:
        db.refresh(trade)
    return created


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