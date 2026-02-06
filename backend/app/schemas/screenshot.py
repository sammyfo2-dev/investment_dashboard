from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ScreenshotUploadResponse(BaseModel):
    id: int
    extracted_text: str
    tickers_mentioned: list[str]
    investment_thesis: str
    upload_timestamp: datetime


class AIAnalysisResponse(BaseModel):
    id: int
    ai_analysis: str
    recommendation: str
    risk_rating: str
    analysis_cost: float
    analyzed_at: datetime


class ScreenshotResponse(BaseModel):
    id: int
    image_path: str
    upload_timestamp: datetime
    extracted_text: Optional[str] = None
    tickers_mentioned: list[str] = []
    investment_thesis: Optional[str] = None
    ai_analyzed: bool = False
    ai_analysis: Optional[str] = None
    recommendation: Optional[str] = None
    risk_rating: Optional[str] = None
    analysis_cost: Optional[float] = None
    analyzed_at: Optional[datetime] = None

    class Config:
        from_attributes = True
