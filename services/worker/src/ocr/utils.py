import os
import shutil
from pdf2image import convert_from_path
from pikepdf import Pdf
import logging
import tempfile 
from src.ocr.pdf_dpi import calculate_image_dpi

logger = logging.getLogger(__name__)

def rasterize_pdf(input_pdf_path, output_pdf_path, dpi=300):
    ## Use this rasterize for upsampling because ideally don't just want to upscale pdf text but as image!
    #- see silver_test_ocr for evaluations.  @400 better then 300. 8000 too big. 600 not bad.
    
    logger.info(f"Rasterizing: {input_pdf_path}")
    # Convert each page of the PDF to an image
    with tempfile.TemporaryDirectory() as temp_dir:
        images = convert_from_path(input_pdf_path, dpi=dpi, output_folder=temp_dir)
        logger.info("Images converted")
        # Save the images as a single PDF
        images[0].save(output_pdf_path, "PDF", resolution=dpi, save_all=True, append_images=images[1:])
        out_dpi = calculate_image_dpi(output_pdf_path)
        logger.info(f"Rasterized: {output_pdf_path} at {out_dpi}")

    return

def alg_decrypt_pdf(input_filename,output_filename=None):
    ## Assume in-place conversion
    is_encrypted=False
    did_decryption=False
    
    if not output_filename:
        output_filename=input_filename
    
    if not os.path.exists(input_filename):
        raise Exception("File does not exist: "+str(input_filename))

    with Pdf.open(input_filename,allow_overwriting_input=True) as pdf:
        is_encrypted=pdf.is_encrypted
        if is_encrypted:
            logging.info("[file is encrypted]: "+str(input_filename))
            pdf.save(output_filename)
            did_decryption=True
        else:
            if not input_filename==output_filename:
                shutil.copyfile(input_filename,output_filename)

    return is_encrypted,did_decryption,output_filename

