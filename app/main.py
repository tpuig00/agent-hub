import logging

from fastapi import FastAPI

from app.api.routes import router as messages_router
from app.config import settings

logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

app = FastAPI()
app.include_router(messages_router)


@app.get("/")
def home():
    return {"message": "API funcionando"}
