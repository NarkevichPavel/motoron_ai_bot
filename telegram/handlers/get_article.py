import os

from aiogram import Router, F, Bot
from aiogram.enums import ParseMode
from aiogram.types import Message

import re

import pytesseract

from PIL import Image

main_router = Router(name=__name__)


@main_router.message(F.photo)
async def get_article(message: Message, bot: Bot):
    file = await bot.get_file(message.photo[-1].file_id)

    save_path = 'C:/Users/Тимофей/PycharmProjects/pythonProject/images/'

    file_path = os.path.join(save_path, f'{file.file_unique_id}.png')

    await bot.download_file(file.file_path, destination=file_path)

    image = Image.open(f"images/{file.file_unique_id}.png")

    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    text = pytesseract.image_to_string(image, lang='rus')

    pattern = r"Артикул:\s*(\d+)"
    match = re.search(pattern, text)

    if match:
        text = f"<a href='https://motoron.by/finder?ajaxDiv=%23filter&brand=&model=&partName=&driveV=&gas=0&q={match.group(1)}'>{match.group(1)}</a>"
        return await message.answer(text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

    pattern = r"Арт:\s*(\d+)"

    matches = re.findall(pattern, text)

    if matches:
        if len(matches) == 1:
            text = f"<a href='https://motoron.by/finder?ajaxDiv=%23filter&brand=&model=&partName=&driveV=&gas=0&q={matches[0]}'>{matches[0]}</a>"
            return await message.answer(text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        else:
            for article in matches:
                text = f"<a href='https://motoron.by/finder?ajaxDiv=%23filter&brand=&model=&partName=&driveV=&gas=0&q={article}'>{article}</a>"
                await message.answer(text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
