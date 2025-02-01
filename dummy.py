from sqlalchemy.orm import Session
from datetime import datetime
from app.models import Category, ReviewHistory, AccessLog
from app.database import SessionLocal, engine, Base

# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)

def create_dummy_data():
    # Create a new session
    session = SessionLocal()
    try:
        # Add Categories
        category1 = Category(name="Technology", description="Reviews related to tech products.")
        category2 = Category(name="Books", description="Book reviews.")
        category3 = Category(name="Movies", description="Movie reviews.")

        session.add_all([category1, category2, category3])
        session.commit()

        # Add Review Histories
        review1 = ReviewHistory(
            text="Great phone with amazing battery life!",
            stars=5,
            review_id="rev_001",
            tone="Positive",
            sentiment="Happy",
            category_id=category1.id
        )

        review2 = ReviewHistory(
            text="The plot was dull and uninspiring.",
            stars=2,
            review_id="rev_002",
            tone="Negative",
            sentiment="Disappointed",
            category_id=category3.id
        )

        session.add_all([review1, review2])
        session.commit()

        # Add Access Logs
        log1 = AccessLog(
            text="User accessed the review page.",
            created_at=datetime.utcnow()
        )

        log2 = AccessLog(
            text="Admin updated a review.",
            created_at=datetime.utcnow()
        )

        session.add_all([log1, log2])
        session.commit()

        print("Dummy data inserted successfully!")

    except Exception as e:
        session.rollback()
        print(f"Error inserting dummy data: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    create_dummy_data()
