from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    REDIS_BROKER_URL: str
    OPENAI_API_KEY: str
    DATABASE_URL: str  # Example for database URL
    # Other fields...

    class Config:
        env_file = ".env"  # Tells Pydantic to load variables from the .env file
        env_file_encoding = "utf-8"

settings = Settings()

print(settings.REDIS_BROKER_URL)  # This will print the value from the .env file
print(settings.OPENAI_API_KEY)  