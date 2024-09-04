import re

import pytesseract

from PIL import Image



image = Image.open("images/AQADDOExG4rdQEl-.png")

pytesseract.pytesseract.tesseract_cmd = 'Tesseract-OCR/tesseract.exe'
text = pytesseract.image_to_string(image, lang='rus')
print(text)