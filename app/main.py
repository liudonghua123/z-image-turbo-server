from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api import router
from app.service import service

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load model on startup
    service.load_model()
    yield
    # Clean up (if needed)

app = FastAPI(lifespan=lifespan, title="Z-Image-Turbo Server")

app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok"}
