from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from src.app.generic_exception_handler import generic_exception_handler
from src.logging.logger import setup_logging
from celery import Celery
import uuid

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging("app")
    try:
        yield
    finally:
        pass

app = FastAPI(lifespan=lifespan)

celery_app = Celery(
    'ocr',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)

@app.get("/ping")
async def ping():
    return "ponk"

@app.get("/mvo")
async def mvo():
    file_out = f"{uuid.uuid4()}.pdf"
    print(file_out)
    task = celery_app.send_task('ocr.minimum_viable_ocr', args=[file_out])
    return {"file_out": file_out, "task_id": task.id}

# Used for logging all uncatched exceptions
app.add_exception_handler(Exception, generic_exception_handler)
