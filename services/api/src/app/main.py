from fastapi import FastAPI, Request,  File, UploadFile, HTTPException
from contextlib import asynccontextmanager
from src.app.generic_exception_handler import generic_exception_handler
from src.logging.logger import setup_logging
from celery import Celery
import uuid
import re

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

@app.post("/ocr-file-in")
async def ocr_file_in(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400)

    ### ToDo: Auth validation
    if not file.filename.endswith('.pdf') or file.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")


    file_data = await file.read()
    file_in = file.filename
    file_out = re.sub(r'(.+)(\.pdf)$', r'\1-ocr-standalone\2', file.filename)

    task = celery_app.send_task('ocr.ocr_file_in', args=[file_data, file_in, file_out])

    return {"file_out": file_out, "task_id": task.id}

@app.get("/check-task/{task_id}")
async def check_task(task_id: str):
    task_result = celery_app.AsyncResult(task_id)
    task_data = task_result.get()

    ### Remove the result from the redis queue to save on ram
    task_result.forget()


    return {
        "task_id": task_data.task_id,
        "status": task_data.status,
        "result": task_data.result
    }
    

# Used for logging all uncatched exceptions
app.add_exception_handler(Exception, generic_exception_handler)
