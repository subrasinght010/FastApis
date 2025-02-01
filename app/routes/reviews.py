from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.crud import get_reviews_trends, get_reviews_for_category
from app.schemas import CategoryTrendResponse, ReviewResponse
from app.tasks import log_access#, analyze_tone_and_sentiment, update_review_with_tone_and_sentiment
from app.database import get_db
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter()

@router.get("/reviews/trends", response_model=List[CategoryTrendResponse])
async def reviews_trends(db: Session = Depends(get_db)):
    try:
        trends = get_reviews_trends(db)
    except Exception as e:
        logger.error(f"Error fetching trends: {e}")
        raise HTTPException(status_code=500, detail="Error fetching trends")
    # api_call="GET /reviews/trends"
    task = log_access.apply_async(args=["GET /reviews/trends"])
    task = log_access.apply_async(args=["GET /reviews/trends"])
    from celery.result import AsyncResult

    result = AsyncResult(task.id)

    # Log the result of the task to track progress
    logger.info(f"Task status: {result.status}, result: {result.result}")
    
    return [
        CategoryTrendResponse(
            id=row[0],
            name=row[1],
            description=row[2],
            average_stars=row[3],
            total_reviews=row[4]
        ) for row in trends
    ] if trends else []


@router.get("/reviews/", response_model=List[ReviewResponse])
async def get_reviews(
    category_id: int,
    offset: int = Query(0, ge=0),
    limit: int = Query(15, le=100),
    db: Session = Depends(get_db)
):
    try:
        reviews = get_reviews_for_category(db, category_id, offset, limit)
    except Exception as e:
        logger.error(f"Error fetching reviews: {e}")
        raise HTTPException(status_code=500, detail="Error fetching reviews")
    
    if not reviews:
        raise HTTPException(status_code=404, detail="Reviews not found")

    # Prepare tasks for analysis and updating
    tasks = [
        analyze_tone_and_sentiment.s(review.text, review.stars) | update_review_with_tone_and_sentiment.s(review.id)
        for review in reviews if review.tone == "N/A" or review.sentiment == "N/A"
    ]
    
    if tasks:
        from celery import group
        try:
            group(tasks).apply_async()
        except Exception as e:
            logger.error(f"Error executing tasks: {e}")
            raise HTTPException(status_code=500, detail="Error processing reviews")

    log_access.apply_async([f"GET /reviews/?category_id={category_id}"])

    return reviews
