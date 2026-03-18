from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg2://banking:banking@localhost:5432/banking"
    class Config:
        env_file = ".env"

settings = Settings()
