import logging
from fastapi import FastAPI
from router import api_router

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(name)s:%(lineno)d - %(message)s"
)

app = FastAPI()
app.include_router(api_router)
