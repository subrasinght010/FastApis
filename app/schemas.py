from pydantic import BaseModel
from typing import List, Optional

class ImageSchema(BaseModel):
    product_name: str
    input_url: str
    output_path: Optional[str] = None
    status: str

class FileSchema(BaseModel):
    request_id: str
    filename: str
    status: str
    processed_csv_path: Optional[str] = None
    images: List[ImageSchema] = []
