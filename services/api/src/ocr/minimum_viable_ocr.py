from pikepdf import Pdf
import ocrmypdf
import uuid
from src.worker.celery_app import celery

async def minimum_viable_ocr():
    file_out = f"{uuid.uuid4()}.pdf"
    task = minimum_viable_ocr_task.delay(file_out)
    return {"file_out": file_out, "task_id": task.id}

@celery.task
def minimum_viable_ocr_task(file_out: str):
    ocr = ocrmypdf.ocr("/home/app/test_data/Schoolkidz-December-2021-statement.pdf", f"/home/app/test_data/{file_out}", language='eng',rotate_pages=True, deskew=True, force_ocr=True, jobs=2)
