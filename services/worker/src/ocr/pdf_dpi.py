from collections import Counter
import logging

import fitz # PyMuPDF

from src.logging.logger import setup_logging
setup_logging("celery")
logger = logging.getLogger(__name__)

def has_pdf_been_ocrd_already(pdf_path):
    # {'format': 'PDF 1.6', 'title': '', 'author': '', 'subject': '', 'keywords': '', 'creator': 'OmniPage CSDK 18', 'producer': 'OmniPage 18', 'creationDate': "D:20230828120728-08'00'", 'modDate': '', 'trapped': '', 'encryption': None}
    has_it=False
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print ("[error] Could not open PDF: "+str(pdf_path))
        return False
    # Access the metadata
    metadata = doc.metadata
    
    # .creator: 'OmniPage CSDK 18', 'ReportLab', 
    
    print ("[debug] PDF META: "+str(metadata))

    if 'OCR' in str(metadata): has_it=True
    if 'OmniPage' in str(metadata): has_it=True
    return has_it

def pdf_has_images(pdf_path):
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print ("[error] Could not open PDF: "+str(pdf_path))
        return False
    
    has_images=False
    for i in range(len(doc)):
        # Iterate through each page
        page = doc[i]
        # Get list of images in the page
        image_list = page.get_images(full=True)
        if image_list:
            has_images=True
            break
    return has_images

def calculate_image_dpi(pdf_path):
    # Open the PDF
#    pdf_path='C:/scripts-23/watchtower/DEMO_SET/colin_for_dec_21/Wells Fargo JWM Raw.pdf'
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print ("[error] Could not open PDF: "+str(pdf_path))
        return 0
    
    # Access the metadata
    #metadata = doc.metadata
    #print ("META: "+str(metadata))
    ## {'format': 'PDF 1.6', 'title': '', 'author': '', 'subject': '', 'keywords': '', 'creator': '', 'producer': 'PyPDF2', 'creationDate': '', 'modDate': '', 'trapped': '', 'encryption': None}

    dpi_values = []

    samples=[]
    for i in range(len(doc)):
        # Iterate through each page
        page = doc[i]
        # Get list of images in the page
        image_list = page.get_images(full=True)
        
        for img_index, img in enumerate(image_list, start=1):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image = base_image["image"]

            # Image width and height in pixels
            width_px = base_image["width"]
            height_px = base_image["height"]

            # Image width and height in points (1 point = 1/72 inches)
            width_pt = img[2]
            height_pt = img[3]

            # Convert points to inches
            width_in = width_pt / 72
            height_in = height_pt / 72

            # Calculate DPI
            dpi_width = width_px / width_in
            dpi_height = height_px / height_in

            dpi_values.append((dpi_width, dpi_height))
            
            samples+=[dpi_width]
            
        if len(samples)>10:
            break
            
    doc.close()
    
    ## Get most common samples value
    org_samples=samples
    samples=Counter(samples)
    samples=samples.most_common(1)
    
    try:
        samples=int(samples[0][0])
    except:
        pass #No samples if no image
        print ("[warning] Could not get DPI: "+str(org_samples))
        samples=0
    
    return samples
