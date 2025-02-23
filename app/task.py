import os
import uuid
import aiofiles
import asyncio
import httpx
import pandas as pd
from PIL import Image
from io import BytesIO
from .database import AsyncSessionLocal
from .crud import update_request_status
from .config import settings

# async def async_process_images(request_id: str, file_path: str, webhook_url: str):
#     async with AsyncSessionLocal() as session:
#         df = pd.read_csv(file_path)
#         if "Output Image Urls" not in df.columns:
#             df["Output Image Urls"] = ""

#         tasks = [process_image_row(index, row["Input Image Urls"].split(","), df) for index, row in df.iterrows()]
#         await asyncio.gather(*tasks)

#         processed_csv_path = os.path.join(config.settings.PROCESSED_CSV_FOLDER, f"processed_{request_id}.csv")
#         async with aiofiles.open(processed_csv_path, "w", encoding="utf-8") as f:
#             await f.write(df.to_csv(index=False))

#         await update_request_status(session, request_id, "completed", processed_csv_path)

#         # Trigger webhook
#         await trigger_webhook(request_id, processed_csv_path, webhook_url)

async def async_process_images(request_id: str, file_path: str, webhook_url: str):
    async with AsyncSessionLocal() as session:
        # Read the CSV file asynchronously
        async with aiofiles.open(file_path, mode='r', encoding='utf-8') as f:
            contents = await f.read()

        # Convert the contents to a DataFrame
        from io import StringIO
        df = pd.read_csv(StringIO(contents))

        if "Output Image Urls" not in df.columns:
            df["Output Image Urls"] = ""

        tasks = [process_image_row(index, row["Input Image Urls"].split(","), df) for index, row in df.iterrows()]
        await asyncio.gather(*tasks)

        processed_csv_path = os.path.join(settings.PROCESSED_CSV_FOLDER, f"processed_{request_id}.csv")
        async with aiofiles.open(processed_csv_path, "w", encoding="utf-8") as f:
            await f.write(df.to_csv(index=False))

        await update_request_status(session, request_id, "completed", processed_csv_path)

        # Trigger webhook
        await trigger_webhook(request_id, processed_csv_path, webhook_url)


async def process_image_row(index: int, image_urls: list, df: pd.DataFrame):
    async with httpx.AsyncClient() as client:
        tasks = [download_and_compress_image(client, img_url) for img_url in image_urls]
        results = await asyncio.gather(*tasks)

    df.at[index, "Output Image Urls"] = ",".join(results)

async def download_and_compress_image(client: httpx.AsyncClient, img_url: str) -> str:
    try:
        response = await client.get(img_url, timeout=10)
        response.raise_for_status()
        
        img = Image.open(BytesIO(response.content))
        output_path = os.path.join(settings.PROCESSED_IMAGE_FOLDER, f"{uuid.uuid4()}.jpg")
        await asyncio.to_thread(img.save, output_path, quality=50)
        
        return output_path
    except Exception:
        return ""

async def trigger_webhook(request_id: str, processed_csv_path: str, webhook_url: str):
    """ Sends a webhook notification after processing completion. """
    async with httpx.AsyncClient() as client:
        await client.post(webhook_url, json={
            "request_id": request_id,
            "processed_csv_url": processed_csv_path
        })
