# Setup Verification Checklist

Use this checklist to verify that everything is properly installed and configured.

## File Structure Verification

### Backend Files (Should all exist)
- [x] backend/app/main.py
- [x] backend/app/config.py
- [x] backend/app/api/stocks.py
- [x] backend/app/api/watchlist.py
- [x] backend/app/api/screenshots.py
- [x] backend/app/api/health.py
- [x] backend/app/services/stock_service.py
- [x] backend/app/services/technical_analysis.py
- [x] backend/app/services/ocr_service.py
- [x] backend/app/services/ai_service.py
- [x] backend/app/services/cache_service.py
- [x] backend/app/models/watchlist.py
- [x] backend/app/models/price_history.py
- [x] backend/app/models/moving_averages.py
- [x] backend/app/models/screenshots.py
- [x] backend/requirements.txt
- [x] backend/Dockerfile
- [x] backend/.env

### Frontend Files (Should all exist)
- [x] frontend/src/App.tsx
- [x] frontend/src/main.tsx
- [x] frontend/src/components/tracker/PriceCard.tsx
- [x] frontend/src/components/tracker/TrackerGrid.tsx
- [x] frontend/src/components/tracker/MovingAverageIndicator.tsx
- [x] frontend/src/components/tracker/HighLowRangeBar.tsx
- [x] frontend/src/components/screenshots/ScreenshotUpload.tsx
- [x] frontend/src/components/screenshots/ScreenshotHistory.tsx
- [x] frontend/src/hooks/useStockData.ts
- [x] frontend/src/hooks/useWatchlist.ts
- [x] frontend/src/hooks/useScreenshots.ts
- [x] frontend/src/services/stockService.ts
- [x] frontend/package.json
- [x] frontend/Dockerfile
- [x] frontend/.env

### Root Files (Should all exist)
- [x] docker-compose.yml
- [x] README.md
- [x] START.md
- [x] .gitignore

## Quick File Count

Run these commands to verify:

```bash
# Count Python files (should be ~20)
find backend -name "*.py" | wc -l

# Count TypeScript/React files (should be ~22)
find frontend/src -name "*.tsx" -o -name "*.ts" | wc -l

# Total Python code lines (should be ~1100)
find backend -name "*.py" -exec wc -l {} + | tail -1
```

## Configuration Checklist

### Backend Environment (.env)
Check `backend/.env` has these variables:
- [ ] DATABASE_URL (set to postgres connection string)
- [ ] REDIS_URL (set to redis://localhost:6379)
- [ ] ANTHROPIC_API_KEY (optional, leave empty if not using AI)
- [ ] DEBUG=True
- [ ] UPLOAD_DIR=./uploads

### Frontend Environment (.env)
Check `frontend/.env` has:
- [ ] VITE_API_BASE_URL=http://localhost:8000

## Pre-Flight Checks

Before running `docker-compose up`:

### Docker Desktop
- [ ] Docker Desktop is installed
- [ ] Docker Desktop is running
- [ ] Docker has at least 4GB RAM allocated
- [ ] Docker has at least 20GB disk space available

### Port Availability
Make sure these ports are free:
- [ ] 5432 (PostgreSQL) - No other database running
- [ ] 6379 (Redis) - No other Redis instance
- [ ] 8000 (Backend) - No other API server
- [ ] 5173 (Frontend) - No other dev server

Check with:
```bash
# Windows PowerShell
netstat -ano | findstr ":5432"
netstat -ano | findstr ":6379"
netstat -ano | findstr ":8000"
netstat -ano | findstr ":5173"
```

No output = port is free ✅

## First Run Tests

After running `docker-compose up --build`:

### Container Status
All 4 containers should be running:
```bash
docker-compose ps
```

Expected output:
- postgres (healthy)
- redis (healthy)
- backend (running)
- frontend (running)

### Health Checks

1. **Backend API**
   ```bash
   curl http://localhost:8000/health
   ```
   Expected: `{"status":"healthy","timestamp":"...","service":"Investing Dashboard API"}`

2. **Frontend**
   Open browser: http://localhost:5173
   Expected: Dashboard loads with header

3. **API Documentation**
   Open browser: http://localhost:8000/docs
   Expected: Swagger UI with all endpoints

### Data Verification

1. **Sample Watchlist**
   ```bash
   curl http://localhost:8000/api/watchlist
   ```
   Expected: Array with 8 items (AAPL, GOOGL, MSFT, TSLA, NVDA, BTC-USD, ETH-USD, SOL-USD)

2. **Stock Data**
   ```bash
   curl http://localhost:8000/api/stocks/AAPL
   ```
   Expected: JSON with price, moving_averages, high_low_range

3. **Database Connection**
   ```bash
   docker-compose exec postgres psql -U investing_user -d investing_tool -c "\dt"
   ```
   Expected: List of 4 tables (watchlist, price_history, moving_averages, screenshots)

### Frontend Verification

Open http://localhost:5173 and check:

1. **Price Tracker Tab**
   - [ ] Header shows "Investing Dashboard"
   - [ ] "Price Tracker" tab is active
   - [ ] 8 price cards are displayed in a grid
   - [ ] Each card shows:
     - Stock symbol (e.g., AAPL)
     - Current price in dollars
     - 24h change with up/down arrow
     - 52-week range bar with blue indicator
     - 5 moving averages with green/red colors
     - Distance percentages

2. **Screenshot Analysis Tab**
   - [ ] Click "Screenshot Analysis" tab
   - [ ] Upload zone appears with cloud icon
   - [ ] "Screenshot History" card appears below
   - [ ] Initially shows "No screenshots uploaded yet"

## Functional Tests

### Test 1: Price Data Loading
1. Open Price Tracker tab
2. Wait for all cards to load
3. Verify no error messages
4. Check that prices are reasonable (> $0)
5. Verify moving averages show values or "N/A"

### Test 2: Screenshot Upload (OCR only)
1. Go to Screenshot Analysis tab
2. Take a screenshot of any text with tickers (e.g., "$AAPL is great")
3. Drag screenshot to upload zone
4. Wait 2-5 seconds
5. Verify it appears in history with:
   - Timestamp
   - Extracted tickers (e.g., AAPL)
   - Some extracted text
   - "Analyze with AI" button

### Test 3: AI Analysis (Optional)
Only if ANTHROPIC_API_KEY is set:
1. Upload a screenshot with investment text
2. Click "Analyze with AI" button
3. Wait 5-10 seconds
4. Verify analysis appears with:
   - Recommendation (BUY/HOLD/AVOID)
   - Risk rating (LOW/MEDIUM/HIGH)
   - Analysis text
   - Cost displayed (~$0.10-0.25)

## Common Issues & Solutions

### Issue: "Cannot connect to Docker daemon"
**Solution**: Start Docker Desktop

### Issue: "Port 5432 already in use"
**Solution**:
```bash
# Find and stop the conflicting service
# Or change port in docker-compose.yml
```

### Issue: "Module not found" errors in backend
**Solution**:
```bash
docker-compose down
docker-compose build --no-cache backend
docker-compose up
```

### Issue: Frontend shows blank page
**Solution**:
1. Check browser console for errors
2. Verify backend is running: curl http://localhost:8000/health
3. Check frontend/.env has correct API URL
4. Rebuild: `docker-compose build --no-cache frontend`

### Issue: No data in watchlist
**Solution**:
```bash
# Reinitialize database
docker-compose down -v
docker-compose up
```

### Issue: OCR not extracting text
**Solution**:
1. Check backend logs: `docker-compose logs backend`
2. Ensure Tesseract is installed in container
3. Try with clearer, higher-contrast screenshots

### Issue: AI analysis returns error
**Solution**:
1. Check ANTHROPIC_API_KEY in backend/.env
2. Verify API key format: `sk-ant-...`
3. Check API credits at https://console.anthropic.com/
4. Look at backend logs for detailed error

## Performance Benchmarks

Expected performance:
- Dashboard loads: < 2 seconds
- Stock data fetch: < 1 second per symbol (cached)
- Screenshot OCR: 2-5 seconds
- AI analysis: 5-10 seconds
- Moving average calculation: < 500ms

## Success Criteria

All checks should pass:
- [x] All files present
- [x] Docker containers running
- [x] Backend API responding
- [x] Frontend loads
- [x] Watchlist populated
- [x] Price data displays
- [x] Screenshots upload
- [x] OCR extracts text
- [x] (Optional) AI analysis works

## Final Verification

If all checks pass, you're ready to use the dashboard!

Run this final command to see everything working:
```bash
# Should return sample watchlist
curl -s http://localhost:8000/api/watchlist | python -m json.tool
```

## Need Help?

If something isn't working:
1. Check this file for common issues
2. Look at docker logs: `docker-compose logs`
3. Check backend logs: `docker-compose logs backend`
4. Check frontend logs: `docker-compose logs frontend`
5. Read README.md for detailed documentation
6. Read START.md for setup instructions

## Quick Reset

If you need to start fresh:
```bash
# Stop and remove everything
docker-compose down -v

# Rebuild and start
docker-compose up --build
```

This will:
- Delete all containers
- Delete all volumes (database data)
- Rebuild images from scratch
- Reinitialize with sample data

---

**Status Check**: If you've completed all items above, your dashboard is fully operational!

Start investing with confidence using Charlie Munger's moving average strategy.
