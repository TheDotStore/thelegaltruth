import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io

def pdf_to_ocr_text(filepath):
    # Open the provided PDF file
    doc = fitz.open(filepath)
    text = ''

    for page in doc:
        # Get the page as an image
        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes()))
        
        page_text = pytesseract.image_to_string(img)
        text += page_text

    return text

if __name__ == "__main__":
    filepath = 'ecell.pdf'  # Specify your PDF file path here
    extracted_text = pdf_to_ocr_text(filepath)
    print(extracted_text)
