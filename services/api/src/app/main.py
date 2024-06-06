from fastapi import FastAPI, Request,  File, UploadFile, HTTPException, status
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from src.app.generic_exception_handler import generic_exception_handler
from src.logging.logger import setup_logging
from celery import Celery
import uuid
import re
import aioredis

redis: aioredis.Redis | None = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging("app")
    global redis
    redis = await aioredis.from_url('redis://redis:6379/0')
    try:
        yield
        await redis.close()
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

    if redis:
        await redis.set(file_out, task.id)

    return {"file_out": file_out, "task_id": task.id}

@app.get("/check-task/{file_name_out}")
async def check_task(file_name_out: str):
    """
        Gets the status of the task you created in ocr_file_in, when the task has 
        succeeded will return a b64 encoded string of the document and remove the
        b64 encoded string from the redis queue.
    """
    if not redis:
        raise HTTPException(
                status_code=500,
                detail="Couldn't retrieve connection to Redis"
        )
    
    task_id = await redis.get(file_name_out)

    task = celery_app.AsyncResult(task_id)

    if task.result:
        result = task.get()
        task.forget()

        return FileResponse(result)

    return {
        "task_id": task.task_id,
        "status": task.status,
        "result": task.result
    }


# Used for logging all uncatched exceptions
app.add_exception_handler(Exception, generic_exception_handler)
