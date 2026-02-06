from sqlalchemy.orm import Session
from app.models.watchlist import Watchlist


# Pre-populate with sample assets
SAMPLE_WATCHLIST = [
    # Stocks
    {"symbol": "AAPL", "asset_type": "STOCK", "name": "Apple Inc."},
    {"symbol": "GOOGL", "asset_type": "STOCK", "name": "Alphabet Inc."},
    {"symbol": "MSFT", "asset_type": "STOCK", "name": "Microsoft Corp."},
    {"symbol": "TSLA", "asset_type": "STOCK", "name": "Tesla Inc."},
    {"symbol": "NVDA", "asset_type": "STOCK", "name": "NVIDIA Corp."},

    # Crypto
    {"symbol": "BTC-USD", "asset_type": "CRYPTO", "name": "Bitcoin"},
    {"symbol": "ETH-USD", "asset_type": "CRYPTO", "name": "Ethereum"},
    {"symbol": "SOL-USD", "asset_type": "CRYPTO", "name": "Solana"},
]


def initialize_sample_watchlist(db: Session):
    """Initialize watchlist with sample assets if empty"""
    existing_count = db.query(Watchlist).count()

    if existing_count == 0:
        print("Initializing sample watchlist...")
        for item in SAMPLE_WATCHLIST:
            db_item = Watchlist(**item)
            db.add(db_item)

        db.commit()
        print(f"Added {len(SAMPLE_WATCHLIST)} sample assets to watchlist")
    else:
        print(f"Watchlist already has {existing_count} items")
