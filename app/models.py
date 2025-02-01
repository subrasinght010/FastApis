from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    description = Column(Text)
    
    reviews = relationship("ReviewHistory", back_populates="category")


class ReviewHistory(Base):
    __tablename__ = 'review_history'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=True)
    stars = Column(Integer)
    review_id = Column(String(255), index=True)
    tone = Column(String(255), nullable=True)
    sentiment = Column(String(255), nullable=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = relationship("Category", back_populates="reviews")


class AccessLog(Base):
    __tablename__ = 'access_log'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
