from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.database.session import Base


class MovingAverage(Base):
    __tablename__ = "moving_averages"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), nullable=False, index=True)
    ma_50 = Column(Float)
    ma_100 = Column(Float)
    ma_150 = Column(Float)
    ma_200_day = Column(Float)
    ma_200_week = Column(Float)
    week_52_high = Column(Float)
    week_52_low = Column(Float)
    calculated_at = Column(DateTime(timezone=True), server_default=func.now())
