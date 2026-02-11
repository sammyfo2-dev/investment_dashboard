from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.watchlist import Watchlist
from app.schemas.watchlist import WatchlistCreate, WatchlistResponse, WatchlistUpdate
from app.services.stock_service import StockService
from typing import List

router = APIRouter()


@router.get("", response_model=List[WatchlistResponse])
async def get_watchlist(db: Session = Depends(get_db)):
    """Get all items in watchlist"""
    items = db.query(Watchlist).all()
    return items


@router.post("", response_model=WatchlistResponse)
async def add_to_watchlist(item: WatchlistCreate, db: Session = Depends(get_db)):
    """Add new item to watchlist"""
    symbol_upper = item.symbol.upper()

    # Check if already exists
    existing = db.query(Watchlist).filter(Watchlist.symbol == symbol_upper).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"{item.symbol} is already in watchlist")

    # Validate symbol exists
    if not StockService.validate_symbol(symbol_upper):
        raise HTTPException(status_code=400, detail=f"Invalid symbol: {item.symbol}")

    # Fetch stock info (name and sector)
    # Returns default values if rate limited or unavailable
    stock_info = StockService.get_stock_info(symbol_upper, item.asset_type)

    db_item = Watchlist(
        symbol=symbol_upper,
        asset_type=item.asset_type.upper(),
        name=item.name if item.name else stock_info['name'],
        sector=stock_info['sector']
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item


@router.patch("/{symbol}", response_model=WatchlistResponse)
async def update_watchlist_item(
    symbol: str,
    update_data: WatchlistUpdate,
    db: Session = Depends(get_db)
):
    """Update watchlist item (name and/or sector)"""
    symbol = symbol.upper()
    item = db.query(Watchlist).filter(Watchlist.symbol == symbol).first()

    if not item:
        raise HTTPException(status_code=404, detail=f"{symbol} not found in watchlist")

    # Update fields if provided
    if update_data.name is not None:
        item.name = update_data.name
    if update_data.sector is not None:
        item.sector = update_data.sector

    db.commit()
    db.refresh(item)

    return item


@router.delete("/{symbol}")
async def remove_from_watchlist(symbol: str, db: Session = Depends(get_db)):
    """Remove item from watchlist"""
    symbol = symbol.upper()
    item = db.query(Watchlist).filter(Watchlist.symbol == symbol).first()

    if not item:
        raise HTTPException(status_code=404, detail=f"{symbol} not found in watchlist")

    db.delete(item)
    db.commit()

    return {"message": f"{symbol} removed from watchlist"}
