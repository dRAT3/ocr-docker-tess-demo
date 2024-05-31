from pdf2image import convert_from_path
import logging

logger = logging.getLogger(__name__)

def rasterize_pdf(input_pdf_path, output_pdf_path, dpi=300):
    ## Use this rasterize for upsampling because ideally don't just want to upscale pdf text but as image!
    #- see silver_test_ocr for evaluations.  @400 better then 300. 8000 too big. 600 not bad.
    
    logger.info(f"Rasterizing: {input_pdf_path}")
    # Convert each page of the PDF to an image
    images = convert_from_path(input_pdf_path, dpi=dpi)

    # Save the images as a single PDF
    images[0].save(output_pdf_path, "PDF", resolution=dpi, save_all=True, append_images=images[1:])
    logger.info("Rasterized: {output_pdf_path}")

    return
