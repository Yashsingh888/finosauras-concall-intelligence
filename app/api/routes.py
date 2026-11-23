
import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.db import get_db
from app.database.models import TranscriptSummary
from app.api.notifications import send_notification


router = APIRouter(
    prefix="/api",
    tags=["Company Summaries"]
)


class NotificationRequest(BaseModel):
    event_type: str
    company_name: str
    message: str


# API 1: Get all company summaries
@router.get("/summaries")
def get_all_summaries(db: Session = Depends(get_db)):

    records = db.query(TranscriptSummary).all()

    results = []

    for record in records:
        results.append({
            "id": record.id,
            "company_name": record.company_name,
            "summary": json.loads(record.summary_json)
            if record.summary_json else {},
            "markdown": record.summary_markdown,
            "created_at": str(record.created_at)
            if record.created_at else None
        })

    return {
        "total": len(results),
        "summaries": results
    }


# API 2: Get summary by company name
@router.get("/summaries/{company_name}")
def get_company_summary(
    company_name: str,
    db: Session = Depends(get_db)
):

    record = db.query(TranscriptSummary).filter(
        TranscriptSummary.company_name.ilike(company_name)
    ).first()

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Company summary not found"
        )

    return {
        "company_name": record.company_name,
        "summary": json.loads(record.summary_json)
        if record.summary_json else {},
        "markdown": record.summary_markdown
    }


# API 3: Publish a WebSocket notification
@router.post("/notifications/publish")
async def publish_notification(data: NotificationRequest):

    await send_notification(
        event_type=data.event_type,
        company_name=data.company_name,
        message=data.message
    )

    return {
        "status": "success",
        "message": "Notification published successfully!"
    }


# API 4: Test real-time notification
@router.post("/notifications/test")
async def test_notification():

    await send_notification(
        event_type="transcript_processed",
        company_name="Frontier Springs Ltd",
        message="Test notification from Finosauras!"
    )

    return {
        "status": "success",
        "message": "Real-time notification sent!"
    }
