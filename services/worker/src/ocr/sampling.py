import os
import shutil
import subprocess
import logging

from src.ocr.pdf_dpi import calculate_image_dpi

logger = logging.getLogger(__name__)

def downsample_pdf(input_pdf, output_pdf, dpi=300):
    #? check if already at 150?
    """
    Processes a PDF file by downsampling images, converting to grayscale, and saving the result.

    :param input_pdf: str, the path to the input PDF file
    :param output_pdf: str or None, the path to the output PDF file (can be the same as input_pdf for overwriting)
    :param dpi: int, the DPI to which images in the PDF should be downsampled
    :return: None
    """
    
    input_pdf = os.path.normpath(os.path.abspath(input_pdf))
    output_pdf = os.path.normpath(os.path.abspath(output_pdf))



    # Check if Ghostscript is installed
    if shutil.which("gs") is None:
        raise Exception("Ghostscript is not installed or not in PATH.")

    if not os.path.exists(input_pdf):
        raise FileNotFoundError(f"Input PDF file {input_pdf} does not exist.")
        
    if output_pdf is None:
        output_pdf = input_pdf

    ## OPTION 1:  writes incomplete file ...maybe color stuff??
    cmd = [
        'gs',
        '-o', output_pdf,
        '-sDEVICE=pdfwrite',
        '-dNOPAUSE',
        '-dQUIET',
        '-dSAFER',
        '-dDownsampleColorImages=true',
        f'-dColorImageResolution={dpi}',
        f'-dGrayImageResolution={dpi}',
        f'-dMonoImageResolution={dpi}',
        '-dColorImageDownsampleThreshold=1.0',
        '-dGrayImageDownsampleThreshold=1.0',
        '-dMonoImageDownsampleThreshold=1.0',
        '-sColorConversionStrategy=Gray',
        '-dProcessColorModel=/DeviceGray',
        input_pdf
    ]
    
    ## OPTION 2:  works (100 pager from 15MB to 5MB looks the same -- likely ocrs the same but faster)
    #[ ] note:  screen PDF setting likely sets to 400 even though asking 300

    cmd = [
    'gs',
    '-o', output_pdf,
    "-sDEVICE=pdfwrite",
    "-dNOPAUSE",
    "-dBATCH",
    "-sColorConversionStrategy=Gray",
    "-dProcessColorModel=/DeviceGray",
    f"-r{dpi}",
    input_pdf
    ]


    logger.info("[OCR.downsampling to: "+str(output_pdf)+"] at "+str(dpi)+" dpi")

    try:
        subprocess.run(cmd, check=True, shell=True)
    except FileNotFoundError:
        print("Error: Ghostscript is not installed or not in the system's PATH.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running Ghostscript: {e}")
    else:
        print("PDF processed successfully.")
        
#    ## CHECK OUTPUT
#    dpi=calculate_image_dpi(output_pdf)
#    print ("[debug] output dpi: "+str(dpi))
    
    # If size of pdf<5kb then throw error
    if os.path.exists(output_pdf):
        size=os.path.getsize(output_pdf)
        if size<5000:
            raise Exception("ERROR: Downsampled PDF is too small: "+str(size)+" bytes")

    return


def upsample_pdf(input_pdf, output_pdf, dpi=600):
    """
    **NOTE:  If text is already text then trying to upsample won't have the desired effect
    
    Processes a PDF file by upsampling images and saving the result.

    :param input_pdf: str, the path to the input PDF file
    :param output_pdf: str or None, the path to the output PDF file (can be the same as input_pdf for overwriting)
    :param dpi: int, the DPI to which images in the PDF should be upsampled
    :return: None
    """
    
    input_pdf = os.path.normpath(os.path.abspath(input_pdf))
    output_pdf = os.path.normpath(os.path.abspath(output_pdf if output_pdf is not None else input_pdf))

    # Check if Ghostscript is installed
    if shutil.which("gs") is None:
        raise Exception("Ghostscript is not installed or not in PATH.")

    if not os.path.exists(input_pdf):
        raise FileNotFoundError(f"Input PDF file {input_pdf} does not exist.")
        
    # Command to upsample images within the PDF
    cmd = [
        'gs',
        '-o', output_pdf,
        "-sDEVICE=pdfwrite",
        "-dNOPAUSE",
        "-dBATCH",
        f"-r{dpi}",
        input_pdf
    ]
    
    ## RASTERIZE no effect.
        #'-dDEBUG',
    cmd = [
        'gs',
        '-o', output_pdf,
        '-sDEVICE=pdfwrite',
        '-dNOPAUSE',
        '-dBATCH',
        '-dPDFSETTINGS=/prepress',  # High quality setting for prepress output
        f'-r{dpi}',  # Set your desired DPI resolution
        input_pdf
    ]

    
    ## when upscale also do greyscale
    if False: #Greyscale options work but no direct effect either
        cmd = [
        'gs',
        '-o', output_pdf,
        "-sDEVICE=pdfwrite",
        "-dNOPAUSE",
        "-dBATCH",
        "-sColorConversionStrategy=Gray",
        "-sProcessColorModel=DeviceGray",
        f"-r{dpi}",
        input_pdf
        ]


    logger.info(f"[OCR.upsampling to: {output_pdf}] at {dpi} dpi")
    print ("[debug] upsample cmd: "+str(" ".join(cmd)))

    try:
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        print("Error: Ghostscript is not installed or not in the system's PATH.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running Ghostscript: {e}")
    else:
        print("PDF processed successfully.")

    ## CHECK OUTPUT
    dpi_output=calculate_image_dpi(output_pdf)
    print ("[debug] output dpi: "+str(dpi_output))
    if dpi_output<dpi:
        #raise Exception("ERROR: Upsampled PDF is too small: "+str(dpi_output)+" dpi expected: "+str(dpi))
        print ("ERROR: Upsampled PDF is too small: "+str(dpi_output)+" dpi expected: "+str(dpi))
        
    # Check the output size
    if os.path.exists(output_pdf):
        size = os.path.getsize(output_pdf)
        if size < 5000:
            raise Exception(f"ERROR: Upsampled PDF is too small: {size} bytes")

    return


