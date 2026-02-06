from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class WatchlistBase(BaseModel):
    symbol: str
    asset_type: str
    name: Optional[str] = None
    sector: Optional[str] = None


class WatchlistCreate(WatchlistBase):
    pass


class WatchlistResponse(WatchlistBase):
    id: int
    name: str
    sector: Optional[str] = None
    added_at: datetime

    class Config:
        from_attributes = True
