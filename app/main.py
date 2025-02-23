from app.database import Base,engine
from fastapi import FastAPI
from .routes import uploads,status

app = FastAPI()

app.include_router(status.router)
app.include_router(uploads.router)

@app.post("/webhook")
async def webhook(payload: dict):
    print(f"WebHook Url : {payload}")
    return {"message": "Webhook received", "payload": payload}
        
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)
