from fastapi import FastAPI

from app.api.routes import router as messages_router

app = FastAPI()
app.include_router(messages_router)


@app.get("/")
def home():
    return {"message": "API funcionando"}
