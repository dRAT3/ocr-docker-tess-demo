from celery import Celery
from src.logging.logger import setup_logging
from src.ocr.pdf_dpi import calculate_image_dpi
from src.ocr.sampling import upsample_pdf, downsample_pdf
from src.ocr.utils import rasterize_pdf
from src.ocr.utils import alg_decrypt_pdf
import logging
import os
import re
import tempfile
import ocrmypdf
import base64

def make_celery(app_name):
    logger = logging.getLogger(__name__)
    logger.info(f"Booting celery worker from {os.getpid()}")
    return Celery(app_name, broker="redis://redis:6379/0", backend="redis://redis:6379/0")


celery_app = make_celery("ocr")

celery_app.conf.update(
    worker_hijack_root_logger=False
)

setup_logging("celery")
logger = logging.getLogger(__name__)

@celery_app.task(name="ocr.minimum_viable_ocr")
def minimum_viable_ocr_task(file_out: str):
    logger.info("Starting minimum viable ocr task")
    ocr = ocrmypdf.ocr("/home/app/test_data/Schoolkidz-December-2021-statement.pdf", f"/home/app/test_data/{file_out}", language='eng',rotate_pages=True, deskew=True, force_ocr=True, jobs=2)
    logger.info("Completed minimum viable ocr task")


@celery_app.task(name="ocr.ocr_file_in")
def ocr_file_in(file_data: bytes, file_in, file_out: str) -> str:
    """
        Will grab the pdf as bytes from the Redis queue. Write to a tempfile and 
        do OCR over it, and return a searchable pdf to the Redis queue. This searchable
        pdf can then be downloaded by the client.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        temp_file.write(file_data)
        temp_file_path = temp_file.name
        ### Currently writing to logs dir for easy download from server, needs to be changed
        out_file_path = f"/home/app/logs/{file_out}"

        try:
            ocr = ocrmypdf.ocr(temp_file_path, out_file_path, language='eng',rotate_pages=True, deskew=True, force_ocr=True, jobs=2)
        except Exception as e:
            str_e=str(e)
            if 'PDF is encrypted' in str_e:
                logging.info("PDF encrypted, decrypting and retrying")
                is_encrypted, did_decryption, _ = alg_decrypt_pdf(temp_file_path)
                if did_decryption:
                    try:
                        ocr = ocrmypdf.ocr(temp_file_path, out_file_path, language='eng',rotate_pages=True, deskew=True, force_ocr=True, jobs=2)
                    except Exception as err:
                        logger.error(f"OCR failed: {err}")
                else:
                    logger.warn(f"PDF decryption failed. is_encrypted:{is_encrypted}")
                    raise Exception("OCR failed: "+str_e) #[1] (count)  out of memory?
            else:
                logger.error("[error] at ocr: "+str_e)
                raise Exception("OCR failed: "+str_e) #[1] (count)  out of memory?
        
        with open(out_file_path, "rb") as file:
            pdf_bytes = file.read()
            b64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')

        return b64_pdf
