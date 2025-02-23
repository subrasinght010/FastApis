from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    REDIS_BROKER_URL: str
    OPENAI_API_KEY: str
    DATABASE_URL: str
    UPLOAD_FOLDER: str = "uploads"
    PROCESSED_IMAGE_FOLDER: str = "processed_images"
    PROCESSED_CSV_FOLDER: str = "processed_csv"
    WEBHOOK_URL: str = "http://localhost:8000/webhook"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Initialize settings
settings = Settings()
