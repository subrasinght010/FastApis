from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Files, Image

async def get_request_by_id(db: AsyncSession, request_id: str):
    """Fetch a processing request by request_id."""
    result = await db.execute(select(Files).filter(Files.request_id == request_id))
    return result.scalars().first()

async def update_request_status(db: AsyncSession, request_id: str, status: str, processed_csv_path: str = None):
    """Update the status of an image processing request."""
    request = await get_request_by_id(db, request_id)
    if request:
        request.status = status
        if processed_csv_path:
            request.processed_csv_path = processed_csv_path
        await db.commit()

async def store_image(db: AsyncSession, request_id: str, product_name: str, input_url: str, output_path: str = None):
    """Insert an image record into the database."""
    new_image = Image(request_id=request_id, product_name=product_name, input_url=input_url, output_path=output_path)
    db.add(new_image)
    await db.commit()

async def get_images_by_request_id(db: AsyncSession, request_id: str):
    """Fetch all images for a specific processing request."""
    result = await db.execute(select(Image).filter(Image.request_id == request_id))
    return result.scalars().all()
