from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api import stocks, watchlist, screenshots, health
from app.tasks.scheduler import start_scheduler, stop_scheduler
from app.database.session import engine
from app.models import Base
from app.models.watchlist import Watchlist
from app.tasks.initialize_watchlist import initialize_sample_watchlist
from app.database.session import SessionLocal
from app.services.stock_service import StockService
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session
import os
from app.config import get_settings

settings = get_settings()

app = FastAPI(
    title="Investing Dashboard API",
    description="API for tracking stocks/crypto with moving averages and screenshot analysis",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(stocks.router, prefix="/api/stocks", tags=["stocks"])
app.include_router(watchlist.router, prefix="/api/watchlist", tags=["watchlist"])
app.include_router(screenshots.router, prefix="/api/screenshots", tags=["screenshots"])

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)


def run_sector_migration(db: Session):
    """Add sector column and backfill existing data"""
    try:
        inspector = inspect(engine)
        columns = [col['name'] for col in inspector.get_columns('watchlist')]

        if 'sector' not in columns:
            print("Adding sector column to watchlist table...")
            db.execute(text("ALTER TABLE watchlist ADD COLUMN sector VARCHAR(50)"))
            db.commit()
            print("Sector column added successfully")

            # Backfill existing records
            print("Backfilling sector data for existing stocks...")
            watchlist_items = db.query(Watchlist).all()

            for item in watchlist_items:
                if item.asset_type.upper() == 'CRYPTO':
                    item.sector = 'Cryptocurrency'
                else:
                    stock_info = StockService.get_stock_info(item.symbol, item.asset_type)
                    if stock_info:
                        item.sector = stock_info['sector']
                    else:
                        item.sector = 'Unknown'

            db.commit()
            print(f"Sector backfill complete for {len(watchlist_items)} items")
        else:
            print("Sector column already exists, skipping migration")
    except Exception as e:
        print(f"Error during sector migration: {e}")
        db.rollback()


@app.on_event("startup")
async def startup_event():
    """Initialize database and start scheduler on startup"""
    print("Starting Investing Dashboard API...")

    # Create tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created")

    # Run sector migration
    db = SessionLocal()
    try:
        run_sector_migration(db)
    finally:
        db.close()

    # Initialize sample watchlist
    db = SessionLocal()
    try:
        initialize_sample_watchlist(db)
    finally:
        db.close()

    # Start scheduler for daily updates
    start_scheduler()

    print("API ready at http://localhost:8000")
    print("API docs at http://localhost:8000/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("Shutting down...")
    stop_scheduler()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Investing Dashboard API",
        "docs": "/docs",
        "health": "/health"
    }
