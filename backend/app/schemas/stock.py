from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MovingAveragesData(BaseModel):
    ma_50: Optional[float] = None
    ma_100: Optional[float] = None
    ma_150: Optional[float] = None
    ma_200_day: Optional[float] = None
    ma_200_week: Optional[float] = None


class HighLowRange(BaseModel):
    week_52_high: Optional[float] = None
    week_52_low: Optional[float] = None
    current_price: float
    position_percent: Optional[float] = None  # Position in 52-week range (0-100)


class StockData(BaseModel):
    symbol: str
    name: str
    current_price: float
    change_24h: Optional[float] = None
    change_24h_percent: Optional[float] = None
    moving_averages: MovingAveragesData
    high_low_range: HighLowRange
    last_updated: datetime


class PricePoint(BaseModel):
    date: datetime
    price: float


class StockChartData(BaseModel):
    symbol: str
    prices: list[PricePoint]
