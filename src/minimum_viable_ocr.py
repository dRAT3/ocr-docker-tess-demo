from pikepdf import Pdf
import ocrmypdf

def minimum_viable_ocr() -> str:
    
    ocrmypdf.ocr("/app/test_data/sample.pdf", "/app/test_data/out.pdf", language='eng',rotate_pages=True, deskew=True, force_ocr=True, jobs=2)
    return "OK"


if __name__=='__main__':
    print("Running minimum_viable_ocr.py")
    print(minimum_viable_ocr())
