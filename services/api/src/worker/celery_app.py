from celery import Celery
from src.logging.logger import setup_logging
import logging
import os

from pikepdf import Pdf
import ocrmypdf

def make_celery(app_name=__name__):
    logger = logging.getLogger(__name__)
    logger.info("Booting celery worker from {os.getpid()}")
    return Celery(app_name, broker="redis://redis:6379/0", backend="redis://redis:6379/0")

setup_logging("celery")
celery = make_celery()

@celery.task
def minimum_viable_ocr_task(file_out: str):
    logger = logging.getLogger(__name__)
    logger.info("Starting minimum viable ocr task")
    ocr = ocrmypdf.ocr("/home/app/test_data/Schoolkidz-December-2021-statement.pdf", f"/home/app/test_data/{file_out}", language='eng',rotate_pages=True, deskew=True, force_ocr=True, jobs=2)
    logger.info("Completed minimum viable ocr task")

