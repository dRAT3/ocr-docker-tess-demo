from celery import Celery
from src.logging.logger import setup_logging
import logging

def make_celery(app_name=__name__):
    logger = logging.getLogger(__name__)
    logger.info("Booting celery worker")
    return Celery(app_name, broker="redis://redis:6379/0", backend="redis://redis:6379/0")

setup_logging("celery")
celery = make_celery()
