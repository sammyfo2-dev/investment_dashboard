# Investing Dashboard

A daily-check investing dashboard with two main features:
1. **Price Tracker**: Track stocks/crypto relative to 52-week highs/lows and multiple moving averages (Charlie Munger strategy)
2. **Screenshot Analysis**: Extract investment ideas from X (Twitter) screenshots with optional AI analysis

## Features

### Price Tracker
- Real-time price tracking for stocks and crypto
- 52-week high/low range with visual position indicator
- Moving averages: 50, 100, 150, 200-day, and 200-week
- Color-coded signals (green when above MA, red when below)
- Daily automatic updates

### Screenshot Analysis
- **Free OCR**: Extract tickers and investment thesis from screenshots (Tesseract)
- **Optional AI Analysis**: Deep analysis with Claude API (~$0.10-0.25 per screenshot)
- Cost tracking for AI usage
- Screenshot history and management

## Tech Stack

- **Frontend**: React 18 + TypeScript, Vite, Tailwind CSS
- **Backend**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL with TimescaleDB
- **Cache**: Redis
- **Data Sources**: yfinance (free), CoinGecko API (free)
- **OCR**: Tesseract (free)
- **AI**: Anthropic Claude API (optional)

## Setup Instructions

### Prerequisites
- Docker and Docker Compose
- (Optional) Anthropic API key for AI analysis

### 1. Clone and Setup

```bash
cd Investing_Tool
```

### 2. Configure Environment Variables

**Backend:**
```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env` and add your Anthropic API key if you want AI analysis (optional):
```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**Frontend:**
```bash
cp frontend/.env.example frontend/.env
```

The frontend `.env` should already have the correct API URL:
```
VITE_API_BASE_URL=http://localhost:8000
```

### 3. Start with Docker Compose

```bash
docker-compose up --build
```

This will start:
- PostgreSQL (port 5432)
- Redis (port 6379)
- Backend API (port 8000)
- Frontend (port 5173)

### 4. Access the Dashboard

Open your browser to:
- **Dashboard**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs

The app comes pre-populated with a sample watchlist:
- Stocks: AAPL, GOOGL, MSFT, TSLA, NVDA
- Crypto: BTC-USD, ETH-USD, SOL-USD

## Usage

### Daily Price Check (5 minutes)
1. Open http://localhost:5173
2. View all watchlist assets with updated prices
3. Check which stocks are near key moving averages
4. Identify stocks at 52-week highs/lows
5. Review color-coded signals

### Screenshot Processing

**Free Tier** (process many):
1. See investment idea on X/Twitter
2. Take screenshot (Win+Shift+S on Windows)
3. Drag to dashboard
4. Instantly see: tickers mentioned, key investment thesis
5. Add interesting tickers to watchlist

**Paid Tier** (selective use):
1. For promising opportunities, click "Analyze with AI"
2. Wait ~10 seconds
3. Review detailed analysis with recommendation
4. Cost: ~$0.10-0.25 per analysis

## Cost Breakdown

### Monthly Costs
- **Hosting**: $0 (localhost)
- **yfinance API**: $0 (free)
- **CoinGecko API**: $0 (free tier)
- **Tesseract OCR**: $0 (free, open source)
- **Claude API**: $0-5/month (only for AI analysis)

**Total**: $0-5/month depending on AI usage

## Project Structure

```
Investing_Tool/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── services/     # Business logic
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   └── tasks/        # Background jobs
│   └── uploads/          # Screenshot storage
├── frontend/             # React frontend
│   └── src/
│       ├── components/   # UI components
│       ├── hooks/        # React hooks
│       ├── services/     # API services
│       └── types/        # TypeScript types
└── docker-compose.yml    # Docker orchestration
```

## Development

### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

### Stock Data
- `GET /api/stocks/{symbol}` - Get stock data with technical analysis
- `GET /api/stocks/{symbol}/chart` - Get price history for charting
- `GET /api/stocks/{symbol}/signals` - Get trading signals

### Watchlist
- `GET /api/watchlist` - Get all watchlist items
- `POST /api/watchlist` - Add item to watchlist
- `DELETE /api/watchlist/{symbol}` - Remove item from watchlist

### Screenshots
- `POST /api/screenshots/upload` - Upload and OCR screenshot (free)
- `POST /api/screenshots/{id}/analyze` - Analyze with AI (paid)
- `GET /api/screenshots` - Get all screenshots
- `DELETE /api/screenshots/{id}` - Delete screenshot

## Troubleshooting

### Backend won't start
- Check if PostgreSQL and Redis are running
- Verify DATABASE_URL and REDIS_URL in .env

### Frontend can't connect to backend
- Ensure backend is running on port 8000
- Check VITE_API_BASE_URL in frontend/.env

### OCR not working
- Tesseract is installed in Docker container automatically
- For local development, install Tesseract: `apt-get install tesseract-ocr`

### AI analysis fails
- Check if ANTHROPIC_API_KEY is set correctly
- Verify API key is valid and has credits

## Future Enhancements

- [ ] Add price alerts when crossing moving averages
- [ ] Portfolio tracking (not just watchlist)
- [ ] Backtesting of Charlie Munger strategy
- [ ] Export analysis reports to PDF
- [ ] Mobile-responsive design improvements
- [ ] Deploy to cloud for remote access

## License

MIT

## Support

For issues or questions, please open an issue on GitHub.
