
import io
from fastapi import UploadFile
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

async def run_ocr(file: UploadFile) -> str:
    data = await file.read()
    img = Image.open(io.BytesIO(data))
    text = pytesseract.image_to_string(img, lang='chi_sim+eng')
    return text.strip()
