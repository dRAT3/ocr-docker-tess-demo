from pikepdf import Pdf
import ocrmypdf
import uuid
import logging
from src.worker.celery_app import minimum_viable_ocr_task 

async def minimum_viable_ocr():
    file_out = f"{uuid.uuid4()}.pdf"
    task = minimum_viable_ocr_task.delay(file_out)
    return {"file_out": file_out, "task_id": task.id}
