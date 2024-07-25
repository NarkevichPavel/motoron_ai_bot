import re

import pytesseract

from PIL import Image



image = Image.open("images/AQAD1doxG-ZqqEh-.png")

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
text = pytesseract.image_to_string(image, lang='rus')

print(text)
    # pattern = r"Артикул:\s*(\d+)"
    # match = re.search(pattern, text)
    #
    # if match:
    #     return match.group(1)
    #
    # pattern = r"Арт:\s*(\d+)"
    #
    # matches = re.findall(pattern, text)
    #
    # if matches:
    #     return matches
