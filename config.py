import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./app.db')
    PREMIUM_DEDUCTION_TIME = os.getenv('PREMIUM_DEDUCTION_TIME', '00:00')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    @classmethod
    def validate(cls):
        if not cls.DATABASE_URL:
            raise ValueError("DATABASE_URL environment variable is required")
