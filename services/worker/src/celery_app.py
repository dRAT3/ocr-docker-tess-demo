from celery import Celery
from src.logging.logger import setup_logging
from src.ocr.pdf_dpi import calculate_image_dpi
from src.ocr.sampling import upsample_pdf, downsample_pdf
from src.ocr.utils import rasterize_pdf
import logging
import os
import re
import tempfile
import ocrmypdf


def make_celery(app_name):
    logger = logging.getLogger(__name__)
    logger.info(f"Booting celery worker from {os.getpid()}")
    return Celery(app_name, broker="redis://redis:6379/0", backend="redis://redis:6379/0")


celery_app = make_celery("ocr")

celery_app.conf.update(
    worker_hijack_root_logger=False
)

setup_logging("celery")

@celery_app.task(name="ocr.minimum_viable_ocr")
def minimum_viable_ocr_task(file_out: str):
    logger = logging.getLogger(__name__)
    logger.info("Starting minimum viable ocr task")
    ocr = ocrmypdf.ocr("/home/app/test_data/Schoolkidz-December-2021-statement.pdf", f"/home/app/test_data/{file_out}", language='eng',rotate_pages=True, deskew=True, force_ocr=True, jobs=2)
    logger.info("Completed minimum viable ocr task")


@celery_app.task(name="ocr.ocr_file_in")
def ocr_file_in(file_data: bytes, file_in, file_out: str):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        temp_file.write(file_data)
        temp_file_path = temp_file.name

        ocr = ocrmypdf.ocr(temp_file_path, f"/home/app/logs/{file_out}", language='eng',rotate_pages=True, deskew=True, force_ocr=True, jobs=2)
