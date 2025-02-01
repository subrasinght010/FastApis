from sqlalchemy.orm import Session
from sqlalchemy import func
from .models import ReviewHistory, Category
from typing import List


def get_reviews_trends(db: Session):
    return db.query(
        Category.id,
        Category.name,
        Category.description,
        func.avg(ReviewHistory.stars).label('average_stars'),
        func.count(ReviewHistory.id).label('total_reviews')
    ).join(ReviewHistory).group_by(Category.id).order_by(func.avg(ReviewHistory.stars).desc()).limit(5).all()


def get_reviews_for_category(db: Session, category_id: int, offset: int, limit: int):
    return db.query(ReviewHistory).filter(ReviewHistory.category_id == category_id).order_by(ReviewHistory.created_at.desc()).offset(offset).limit(limit).all()
