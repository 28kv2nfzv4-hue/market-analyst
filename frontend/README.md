# Atlas Trading Dashboard (frontend)

A React + Vite + Tailwind CSS dashboard for the Trading Intelligence Platform. Reads trades from the FastAPI backend's `GET /trades` endpoint.

## Stack

- **React 19** + **Vite** — app shell and dev server
- **Tailwind CSS v4** (via `@tailwindcss/vite`) — styling, no separate PostCSS config needed
- **lucide-react** — icon set used across the sidebar, header, and summary cards

## Setup

```bash
cd frontend
npm install
cp .env.example .env   # optional, defaults to http://127.0.0.1:8000
npm run dev
```

The dashboard runs at `http://localhost:5173`.

## Requirements

The backend must be running with CORS enabled for `http://localhost:5173` (already configured in `backend/main.py`):

```bash
cd ../backend
source .venv/bin/activate
uvicorn main:app --reload
```

## Configuration

`VITE_API_URL` (see `.env.example`) sets the backend base URL. Defaults to `http://127.0.0.1:8000` if unset.

## Structure

```
src/
  api/trades.js         fetch wrapper for GET /trades
  components/
    Sidebar.jsx          nav shell
    Header.jsx           page title + refresh button
    SummaryCards.jsx      total / wins / losses / pending counts
    SummaryCard.jsx        single stat card
    TradesTable.jsx        trades table
    StatusBadge.jsx        direction/result badges
    LoadingState.jsx       spinner state
    ErrorState.jsx         error + retry state
  App.jsx                layout + data fetching
```

## Build

```bash
npm run build   # outputs to dist/
npm run preview # serve the production build locally
```
