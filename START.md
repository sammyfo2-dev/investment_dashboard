# Quick Start Guide

## First Time Setup

1. **Install Prerequisites**
   - Install Docker Desktop for Windows
   - (Optional) Get Anthropic API key from https://console.anthropic.com/

2. **Configure API Key (Optional)**
   - Open `backend/.env`
   - Add your Anthropic API key: `ANTHROPIC_API_KEY=sk-ant-your-key-here`
   - If you skip this, screenshot OCR will still work (free), but AI analysis won't be available

3. **Start the Application**
   ```bash
   docker-compose up --build
   ```

   This will:
   - Download and build all images (first time only, takes ~5-10 minutes)
   - Start PostgreSQL, Redis, Backend, and Frontend
   - Automatically create database tables
   - Initialize sample watchlist with 8 assets

4. **Access the Dashboard**
   - Open browser: http://localhost:5173
   - You'll see the dashboard with sample stocks and crypto

## Daily Usage

```bash
# Start the application
docker-compose up

# Stop the application (Ctrl+C or)
docker-compose down
```

## Without Docker (Local Development)

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Start PostgreSQL and Redis separately, then:
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Troubleshooting

### Port Already in Use
If you get "port already in use" errors:
- 5432: Stop other PostgreSQL instances
- 6379: Stop other Redis instances
- 8000: Stop other backend services
- 5173: Stop other Vite dev servers

### Docker Issues
```bash
# Reset everything
docker-compose down -v
docker-compose up --build
```

### Can't Connect to API
- Make sure backend is running: http://localhost:8000/health
- Check VITE_API_BASE_URL in frontend/.env

## Features

### Price Tracker Tab
- View all watchlist stocks/crypto
- Green indicators = price above moving average (bullish)
- Red indicators = price below moving average (bearish)
- See 52-week range with current position

### Screenshot Analysis Tab
1. Drag & drop screenshots from X/Twitter
2. OCR extracts tickers and text instantly (free)
3. Click "Analyze with AI" for deep analysis (~$0.10-0.25)
4. View all past screenshots and analyses

## Managing Your Watchlist

Currently includes sample assets:
- AAPL, GOOGL, MSFT, TSLA, NVDA (stocks)
- BTC-USD, ETH-USD, SOL-USD (crypto)

To add/remove assets, use the API directly for now:

### Add to Watchlist
```bash
curl -X POST http://localhost:8000/api/watchlist \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AMZN", "asset_type": "STOCK", "name": "Amazon.com Inc."}'
```

### Remove from Watchlist
```bash
curl -X DELETE http://localhost:8000/api/watchlist/AMZN
```

## Next Steps

- Let the app run overnight to test daily price updates (6 AM)
- Upload some investment screenshots to test OCR
- Try AI analysis on interesting opportunities
- Monitor your total AI costs in the database

Enjoy tracking your investments!
