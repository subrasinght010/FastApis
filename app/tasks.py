import logging
from celery import Celery
from .models import AccessLog, ReviewHistory
from .database import SessionLocal
from datetime import datetime
import openai
import os
from typing import Optional

# Celery app initialization
app = Celery('tasks', broker='redis://localhost:6379/0',task_serializer='json')

# Configure logging to write to a file
log_file = "./celery_log.log"  # You can change the file name or path as needed
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Logs to console
        logging.FileHandler(log_file)  # Logs to file
    ]
)

logger = logging.getLogger(__name__)

# Set OpenAI API key from environment variable
# openai.api_key = os.getenv("OPENAI_API_KEY")

# def analyze_sentiment(text: str, stars: int) -> (str, str):
#     prompt = f"Analyze the following review text with stars {stars}. Provide tone and sentiment (positive/neutral/negative):\n\n{text}"
#     try:
#         response = openai.Completion.create(
#             engine="text-davinci-003",
#             prompt=prompt,
#             max_tokens=60
#         )
#         tone = response.choices[0].text.strip()
#         sentiment = "positive" if "good" in tone or "excellent" in tone else "negative"
#         return tone, sentiment
#     except Exception as e:
#         logger.error(f"Error analyzing sentiment: {e}")
#         return "N/A", "N/A"

# Task to log access
@app.task
def log_access(api_call: str):
    try:
        logger.info(f"Received API call: {api_call}")  # Log the input
        db = SessionLocal()
        db.add(AccessLog(text=str(api_call), created_at=datetime.utcnow()))
        db.commit()
        db.close()
        logger.info(f"Access successfully logged for: {api_call}")
    except Exception as e:
        logger.error(f"Error logging access: {e}")
        db.close()  # Ensure the session is closed in case of an error


# Task to analyze tone and sentiment
# @app.task
# def analyze_tone_and_sentiment(text: str, stars: int):
#     try:
#         tone, sentiment = analyze_sentiment(text, stars)
#         logger.info(f"Analyzed sentiment: {tone}, {sentiment}")
#         return tone, sentiment
#     except Exception as e:
#         logger.error(f"Error analyzing tone and sentiment: {e}")
#         return "N/A", "N/A"  # Ensure a return value even in case of an error

# # Task to update review with tone and sentiment
# @app.task
# def update_review_with_tone_and_sentiment(review_id: int, tone: str, sentiment: str):
#     try:
#         db = SessionLocal()
#         review = db.query(ReviewHistory).filter(ReviewHistory.id == review_id).first()
#         if review:
#             review.tone = tone
#             review.sentiment = sentiment
#             db.commit()
#             logger.info(f"Updated review {review_id} with tone: {tone}, sentiment: {sentiment}")
#         db.close()
#     except Exception as e:
#         logger.error(f"Error updating review {review_id}: {e}")
#         return None  # Ensure a return value even in case of an error
