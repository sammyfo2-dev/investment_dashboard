from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Investing Dashboard API"
    }
