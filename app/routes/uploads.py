from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks, HTTPException
import uuid
import os
import aiofiles
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..models import Files
from ..task import async_process_images
from ..utils import validate_csv
from app.config import settings

router = APIRouter()

@router.post("/upload/")
async def upload_csv(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    request_id = str(uuid.uuid4())
    file_path = os.path.join(settings.UPLOAD_FOLDER, f"{request_id}_{file.filename}")

    # Save file asynchronously
    async with aiofiles.open(file_path, "wb") as buffer:
        while chunk := await file.read(1024 * 1024):
            await buffer.write(chunk)

    # Validate CSV
    is_valid, error_message = validate_csv(file_path)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_message)

    # Store request in DB
    new_request = Files(request_id=request_id, filename=file.filename, status="pending")
    db.add(new_request)
    await db.commit()

    # Start async processing
    background_tasks.add_task(async_process_images, request_id, file_path, settings.WEBHOOK_URL)
    
    return {"request_id": request_id}
