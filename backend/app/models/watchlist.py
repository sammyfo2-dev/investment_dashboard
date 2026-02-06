from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database.session import Base


class Watchlist(Base):
    __tablename__ = "watchlist"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), unique=True, index=True, nullable=False)
    asset_type = Column(String(20), nullable=False)  # 'STOCK' or 'CRYPTO'
    name = Column(String(100), nullable=False)
    sector = Column(String(50), nullable=True)
    added_at = Column(DateTime(timezone=True), server_default=func.now())
