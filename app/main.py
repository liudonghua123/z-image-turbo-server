import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api import router
from app.service import service

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load model on startup
    service.load_model()
    # Start the worker
    worker_task = asyncio.create_task(service.start_worker())
    yield
    # Clean up
    print("Shutting down worker...")
    worker_task.cancel()
    try:
        await worker_task
    except asyncio.CancelledError:
        print("Worker shut down gracefully")

app = FastAPI(lifespan=lifespan, title="Z-Image-Turbo Server")

app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok"}
