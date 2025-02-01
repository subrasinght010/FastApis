# # Ensure the verify_data_insertion function is called in your script
# from sqlalchemy.orm import Session
# from app.database import SessionLocal
# from app.models import AccessLog

# def verify_data_insertion():
#     db = SessionLocal()
#     try:
#         logs = db.query(AccessLog).all()
#         if logs:
#             for log in logs:
#                 print(f"Log ID: {log.id}, Text: {log.text}, Created At: {log.created_at}")
#         else:
#             print("No logs found in the database.")
#     except Exception as e:
#         print(f"Error fetching logs: {e}")
#     finally:
#         db.close()

# # Call the function to verify the inserted data
# verify_data_insertion()


from app.database import SessionLocal
from app.models import AccessLog
from datetime import datetime

db = SessionLocal()
new_log = AccessLog(text="Test API call", created_at=datetime.utcnow())
db.add(new_log)
db.commit()
db.close()
