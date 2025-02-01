from fastapi import FastAPI
from .routes import reviews
from .database import engine, Base

# Initialize FastAPI
app = FastAPI()

# Create all tables
Base.metadata.create_all(bind=engine)

# Include the reviews router
app.include_router(reviews.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8001, reload=True)
