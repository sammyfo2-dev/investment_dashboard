from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.screenshots import Screenshot
from app.schemas.screenshot import ScreenshotUploadResponse, AIAnalysisResponse, ScreenshotResponse
from app.services.ocr_service import ocr_service
from app.services.ai_service import ai_service
from datetime import datetime
import os
import uuid
from typing import List
from app.config import get_settings

settings = get_settings()
router = APIRouter()


@router.post("/upload", response_model=ScreenshotUploadResponse)
async def upload_screenshot(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload screenshot and extract text using OCR (free)
    """
    # Validate file type
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")

    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1] or '.png'
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)

    # Ensure upload directory exists
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    # Save file
    try:
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    # Extract text using OCR (free)
    extracted_text = ocr_service.extract_text_from_screenshot(file_path)

    # Extract tickers
    tickers = ocr_service.extract_tickers(extracted_text)

    # Extract investment thesis
    investment_thesis = ocr_service.extract_investment_thesis(extracted_text)

    # Save to database
    screenshot = Screenshot(
        image_path=file_path,
        extracted_text=extracted_text,
        tickers_mentioned=tickers,
        investment_thesis=investment_thesis,
    )

    db.add(screenshot)
    db.commit()
    db.refresh(screenshot)

    return ScreenshotUploadResponse(
        id=screenshot.id,
        extracted_text=extracted_text,
        tickers_mentioned=tickers,
        investment_thesis=investment_thesis,
        upload_timestamp=screenshot.upload_timestamp,
    )


@router.post("/{screenshot_id}/analyze", response_model=AIAnalysisResponse)
async def analyze_screenshot(
    screenshot_id: int,
    db: Session = Depends(get_db)
):
    """
    Trigger AI analysis for a screenshot (paid, ~$0.10-0.25)
    """
    screenshot = db.query(Screenshot).filter(Screenshot.id == screenshot_id).first()
    if not screenshot:
        raise HTTPException(status_code=404, detail="Screenshot not found")

    if screenshot.ai_analyzed:
        # Already analyzed, return cached result
        return AIAnalysisResponse(
            id=screenshot.id,
            ai_analysis=screenshot.ai_analysis,
            recommendation=screenshot.recommendation,
            risk_rating=screenshot.risk_rating,
            analysis_cost=screenshot.analysis_cost,
            analyzed_at=screenshot.analyzed_at,
        )

    # Run AI analysis
    result = await ai_service.deep_analysis(
        screenshot.extracted_text,
        screenshot.tickers_mentioned or []
    )

    if 'error' in result:
        raise HTTPException(status_code=500, detail=result['error'])

    # Update database
    screenshot.ai_analyzed = True
    screenshot.ai_analysis = result['analysis']
    screenshot.recommendation = result['recommendation']
    screenshot.risk_rating = result['risk_rating']
    screenshot.analysis_cost = result['cost']
    screenshot.analyzed_at = datetime.now()

    db.commit()
    db.refresh(screenshot)

    return AIAnalysisResponse(
        id=screenshot.id,
        ai_analysis=screenshot.ai_analysis,
        recommendation=screenshot.recommendation,
        risk_rating=screenshot.risk_rating,
        analysis_cost=screenshot.analysis_cost,
        analyzed_at=screenshot.analyzed_at,
    )


@router.get("", response_model=List[ScreenshotResponse])
async def get_screenshots(db: Session = Depends(get_db)):
    """Get all screenshots with their analysis status"""
    screenshots = db.query(Screenshot).order_by(Screenshot.upload_timestamp.desc()).all()
    return screenshots


@router.get("/{screenshot_id}", response_model=ScreenshotResponse)
async def get_screenshot(screenshot_id: int, db: Session = Depends(get_db)):
    """Get specific screenshot"""
    screenshot = db.query(Screenshot).filter(Screenshot.id == screenshot_id).first()
    if not screenshot:
        raise HTTPException(status_code=404, detail="Screenshot not found")

    return screenshot


@router.delete("/{screenshot_id}")
async def delete_screenshot(screenshot_id: int, db: Session = Depends(get_db)):
    """Delete screenshot"""
    screenshot = db.query(Screenshot).filter(Screenshot.id == screenshot_id).first()
    if not screenshot:
        raise HTTPException(status_code=404, detail="Screenshot not found")

    # Delete file
    if os.path.exists(screenshot.image_path):
        try:
            os.remove(screenshot.image_path)
        except Exception as e:
            print(f"Failed to delete file: {e}")

    # Delete from database
    db.delete(screenshot)
    db.commit()

    return {"message": "Screenshot deleted successfully"}
