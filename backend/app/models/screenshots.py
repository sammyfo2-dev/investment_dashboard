from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, ARRAY
from sqlalchemy.sql import func
from app.database.session import Base


class Screenshot(Base):
    __tablename__ = "screenshots"

    id = Column(Integer, primary_key=True, index=True)
    image_path = Column(String(255), nullable=False)
    upload_timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # OCR extracted (free)
    extracted_text = Column(Text)
    tickers_mentioned = Column(ARRAY(String), default=[])
    investment_thesis = Column(Text)

    # AI analysis (optional, paid)
    ai_analyzed = Column(Boolean, default=False)
    ai_analysis = Column(Text)
    recommendation = Column(String(20))  # 'BUY', 'HOLD', 'AVOID'
    risk_rating = Column(String(20))  # 'LOW', 'MEDIUM', 'HIGH'
    analysis_cost = Column(Float)  # Track costs
    analyzed_at = Column(DateTime(timezone=True))
