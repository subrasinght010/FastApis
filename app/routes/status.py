from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..crud import get_request_by_id

router = APIRouter()

@router.get("/status/{request_id}")
async def get_status(request_id: str, db: AsyncSession = Depends(get_db)):
    request_id = request_id.strip().strip('"')
    request = await get_request_by_id(db, request_id)
    if not request:
        return {"error": "Request not found"}
    return {
        "request_id": request.request_id,
        "status": request.status,
        "processed_csv_url": request.processed_csv_path
    }
