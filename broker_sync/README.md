# Broker Sync (Deriv)

Periodically pulls recently-closed contracts from a Deriv trading account and pushes them into the
backend's trade log via `POST /trades/sync`, so trades don't have to be entered by hand. Runs on a
schedule via `.github/workflows/deriv-sync.yml` rather than as a persistent connection, since this
project has no always-on worker process to host one — Render's free plan is a single web service, and
GitHub Actions cron (already used by `news_bot/`) is the only scheduled-job mechanism in this repo.

**API note (discovered empirically, not from current docs — Deriv's public documentation site is a
JS-rendered SPA that couldn't be scraped for this):** this uses Deriv's newer REST API
(`https://api.derivws.com`), not the classic `wss://ws.derivws.com` WebSocket `authorize` flow, which
returns `InvalidToken` for tokens issued by the current account/developer dashboards regardless of the
token — that flow appears to be deprecated for new tokens. The working endpoint is
`GET /trading/v1/options/legacy/statement`, authenticated via `Authorization: Bearer <token>` +
`Deriv-App-ID: <your registered app_id>` (the public test app_id `1089` is rejected here with
`"Invalid application"` — you need your own app registered at developers.deriv.com). This endpoint
returns a raw transaction ledger (deposits, withdrawals, buys, sells, ...), not pre-paired trade
results — `deriv_sync.py` pairs each `buy` row with its matching `sell` row (same `contract_id`) to
reconstruct a closed trade. Rows with no matching `contract_id` (deposits/withdrawals) or with only a
`buy` and no `sell` yet (still-open positions) are skipped. Duplicate imports are avoided server-side by
`external_id` (the Deriv `contract_id`), so overlapping lookback windows between runs are harmless.

This is a "legacy" endpoint per Deriv's own schema description ("will be removed once the platform
upgrade is complete for all users") — if it stops working at some point, that's expected, and finding
its replacement will require the same kind of live API exploration described above.

## MetaTrader 5 is not supported here

MT5's official Python package (`MetaTrader5`) only talks to a **locally-running MT5 terminal**, normally
on Windows — it has no cloud/REST API for a headless Linux backend like this project's Render service to
call. Supporting MT5 would require standing up a separate always-on bridge machine (e.g. a small Windows
VPS running the terminal + a script that exposes the account data over HTTP) that doesn't exist in this
project. Revisit only if that bridge host gets built.

## Required credentials

| Variable | Where to get it |
|---|---|
| `DERIV_APP_ID` | Register an app at [developers.deriv.com](https://developers.deriv.com/) → Register Application → Native app type. Must be this custom ID, not the public `1089`. |
| `DERIV_API_TOKEN` | Generate at [app.deriv.com/account/api-token](https://app.deriv.com/account/api-token), with all 4 scopes checked (Trade, Account management, Application insights, Payments) — narrower combinations gave `403 Insufficient scopes` on the account this was built against; use a demo account token if you have one to test with first |
| `DERIV_LOGINID` | Your Deriv login ID, e.g. `CR6782045` — find it via the Playground's `GET /trading/v1/options/legacy/accounts` call, or the account switcher on app.deriv.com |
| `BACKEND_API_URL` | Same backend URL used by `news_bot/` |
| `BROKER_SYNC_SECRET` | Must match the backend's `BROKER_SYNC_SECRET` env var |

## Field mapping (Deriv transaction pair → trade log)

Deriv's options/multiplier contracts don't carry a stop-loss/take-profit/risk% the way a retail FX trade
does, so those three fields are sent as `0.0` with an explanatory note. There's also no spot-price data
in this API — `entry_price`/`exit_price` are populated from the stake and payout amounts (in account
currency) instead of an underlying instrument price, which is also called out in the synced trade's
`notes`. See `deriv_sync.py`'s `map_contract_to_trade` for the exact mapping.

## Test locally

```bash
cd broker_sync
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in real values, use a demo account token first
set -a && source .env && set +a
python deriv_sync.py
```

## Test the scheduled workflow without waiting for the cron

```bash
gh workflow run deriv-sync.yml
```

## One-time production database migration

The backend's trade table needs new nullable columns (`source`, `external_id`, `exit_price`,
`profit_loss`, `opened_at`, `closed_at`) before `/trades/sync` will work — `Base.metadata.create_all`
only creates missing tables, it never alters an existing one (no Alembic in this repo). Run once against
the production Postgres:

```sql
ALTER TABLE trades
  ADD COLUMN source VARCHAR,
  ADD COLUMN external_id VARCHAR,
  ADD COLUMN exit_price FLOAT,
  ADD COLUMN profit_loss FLOAT,
  ADD COLUMN opened_at TIMESTAMP,
  ADD COLUMN closed_at TIMESTAMP;
CREATE UNIQUE INDEX IF NOT EXISTS trades_external_id_uidx
  ON trades (external_id) WHERE external_id IS NOT NULL;
```
