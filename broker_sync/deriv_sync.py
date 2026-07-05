import os
import time
from datetime import datetime, timedelta, timezone

import requests

DERIV_API_TOKEN = os.environ["DERIV_API_TOKEN"]
DERIV_APP_ID = os.environ["DERIV_APP_ID"]
DERIV_LOGINID = os.environ["DERIV_LOGINID"]
BACKEND_API_URL = os.environ["BACKEND_API_URL"]
BROKER_SYNC_SECRET = os.environ.get("BROKER_SYNC_SECRET", "")
LOOKBACK_DAYS = int(os.environ.get("DERIV_SYNC_LOOKBACK_DAYS", "2"))

DERIV_API_BASE = "https://api.derivws.com"
STATEMENT_PAGE_LIMIT = 999

# Deriv's options/multiplier contracts don't carry a stop_loss/take_profit/risk%
# the way retail FX trades do -- these fields are sent as 0.0 and explained in `notes`.
DIRECTION_BY_BET_TYPE = {
    "CALL": "buy",
    "MULTUP": "buy",
    "PUT": "sell",
    "MULTDOWN": "sell",
}


def with_retry(fn, *args, retries=3, backoff=2, **kwargs):
    for attempt in range(1, retries + 1):
        try:
            return fn(*args, **kwargs)
        except requests.RequestException:
            if attempt == retries:
                raise
            time.sleep(backoff * attempt)


def deriv_headers():
    return {
        "Deriv-App-ID": DERIV_APP_ID,
        "Authorization": f"Bearer {DERIV_API_TOKEN}",
    }


def fetch_statement_page(date_from, offset):
    def _fetch():
        response = requests.get(
            f"{DERIV_API_BASE}/trading/v1/options/legacy/statement",
            headers=deriv_headers(),
            params={
                "loginid": DERIV_LOGINID,
                "date_from": date_from,
                "limit": STATEMENT_PAGE_LIMIT,
                "offset": offset,
            },
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    return with_retry(_fetch)


def fetch_recent_transactions():
    date_from = int((datetime.now(timezone.utc) - timedelta(days=LOOKBACK_DAYS)).timestamp())
    transactions = []
    offset = 0
    while True:
        page = fetch_statement_page(date_from, offset)
        batch = page.get("transactions", [])
        transactions.extend(batch)
        if len(batch) < STATEMENT_PAGE_LIMIT:
            break
        offset += STATEMENT_PAGE_LIMIT
    return transactions


def pair_closed_contracts(transactions):
    """Statement rows are a raw ledger (buy/sell/deposit/withdrawal/...), one row per
    money movement -- not pre-paired trade results. A closed contract shows up as a
    "buy" row (cost, negative amount) and a later "sell" row (payout, positive amount)
    sharing the same contract_id. We pair them here to reconstruct a trade."""
    buys, sells = {}, {}
    for t in transactions:
        contract_id = t.get("contract_id")
        if contract_id is None:
            continue  # deposit/withdrawal/transfer/etc., not a contract
        if t.get("action_type") == "buy":
            buys[contract_id] = t
        elif t.get("action_type") == "sell":
            sells[contract_id] = t

    closed = []
    for contract_id, buy in buys.items():
        sell = sells.get(contract_id)
        if sell is not None:
            closed.append((contract_id, buy, sell))
    return closed


def map_contract_to_trade(contract_id, buy, sell):
    bet_type = buy.get("bet_type") or sell.get("bet_type") or ""
    direction = DIRECTION_BY_BET_TYPE.get(bet_type)
    if direction is None:
        print(f"Unmapped Deriv bet_type '{bet_type}', defaulting direction to 'buy'")
        direction = "buy"

    stake = float(buy.get("amount", 0))  # negative (cost to open)
    payout = float(sell.get("amount", 0))  # positive (proceeds from close)
    profit = payout + stake

    if profit > 0:
        result = "win"
    elif profit < 0:
        result = "loss"
    else:
        result = "breakeven"

    symbol = buy.get("symbol") or sell.get("symbol") or "UNKNOWN"

    return {
        "pair": symbol,
        "direction": direction,
        "entry_price": abs(stake),
        "stop_loss": 0.0,
        "take_profit": 0.0,
        "risk_percent": 0.0,
        "result": result,
        "notes": (
            f"Auto-synced from Deriv ({bet_type} on {symbol}). "
            "entry_price/exit_price are stake/payout in account currency, not spot "
            "prices. SL/TP/risk% not tracked for this contract type."
        ),
        "source": "deriv",
        "external_id": str(contract_id),
        "exit_price": payout,
        "profit_loss": profit,
        "opened_at": datetime.fromtimestamp(buy["transaction_time"], tz=timezone.utc).isoformat(),
        "closed_at": datetime.fromtimestamp(sell["transaction_time"], tz=timezone.utc).isoformat(),
    }


def push_trades(trades):
    if not trades:
        return

    def _push():
        response = requests.post(
            f"{BACKEND_API_URL}/trades/sync",
            json=trades,
            headers={"X-Broker-Sync-Secret": BROKER_SYNC_SECRET},
            timeout=60,  # Render free tier can take ~30-50s to wake from idle
        )
        response.raise_for_status()
        return response

    with_retry(_push)


def main():
    transactions = fetch_recent_transactions()
    closed_contracts = pair_closed_contracts(transactions)
    if not closed_contracts:
        print("No closed Deriv contracts in the lookback window.")
        return

    trades = [map_contract_to_trade(cid, buy, sell) for cid, buy, sell in closed_contracts]
    push_trades(trades)
    print(f"Synced {len(trades)} Deriv contract(s) to /trades/sync.")


if __name__ == "__main__":
    main()
