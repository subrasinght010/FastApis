from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CategoryTrendResponse(BaseModel):
    id: int
    name: str
    description: str
    average_stars: float
    total_reviews: int

    class Config:
        from_attributes = True  # Updated to match Pydantic V2


class ReviewResponse(BaseModel):
    id: int
    text: str
    stars: int
    review_id: str
    created_at: datetime
    tone: Optional[str] = "N/A"
    sentiment: Optional[str] = "N/A"
    category_id: int

    class Config:
        from_attributes = True  # Updated to match Pydantic V2
