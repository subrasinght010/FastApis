from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Files(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String, unique=True, index=True)
    filename = Column(String)
    status = Column(String, default="pending")
    processed_csv_path = Column(String, nullable=True)

class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String, ForeignKey("files.request_id"))
    product_name = Column(String)
    input_url = Column(String)
    output_path = Column(String, nullable=True)
    status = Column(String, default="Pending")
