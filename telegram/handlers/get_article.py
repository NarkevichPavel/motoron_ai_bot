import os

from aiogram import Router, F, Bot
from aiogram.enums import ParseMode
from aiogram.types import Message
from telegram.handlers.parsing import ParsingIDriver

import re

import pytesseract

from PIL import Image

main_router = Router(name=__name__)


@main_router.message(F.photo)
async def get_article(message: Message, bot: Bot):
    file = await bot.get_file(message.photo[-1].file_id)

    save_path = 'images'

    file_path = os.path.join(save_path, f'{file.file_unique_id}.png')

    await bot.download_file(file.file_path, destination=file_path)

    image = Image.open(f"images/{file.file_unique_id}.png")

    pytesseract.pytesseract.tesseract_cmd = 'Tesseract-OCR/tesseract.exe'
    text = pytesseract.image_to_string(image, lang='rus')

    pattern = r"Артикул:\s*(\d+)"
    match = re.search(pattern, text)

    if match:
        text_note = ParsingIDriver().get_note(article=match.group(1))
        date_last_sale = ParsingIDriver().get_last_action(article=match.group(1), date_find=text_note)

        text = f"<a href='https://motoron.by/finder?ajaxDiv=%23filter&brand=&model=&partName=&driveV=&gas=0&q={match.group(1)}'>{match.group(1)}\nПримечание: {text_note}\n Продажа: {date_last_sale}</a>"

        await message.answer(text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

        os.remove('images/' + f'{file.file_unique_id}.png')
        return

    pattern = r"Арт:\s*(\d+)"

    matches = re.findall(pattern, text)
    if matches:
        text_note = ParsingIDriver().get_note(article=matches[0])
        date_last_sale = ParsingIDriver().get_last_action(article=matches[0], date_find=text_note.lower())
        text = f"<a href='https://motoron.by/finder?ajaxDiv=%23filter&brand=&model=&partName=&driveV=&gas=0&q={matches[0]}'>{matches[0]}\n Примечание: {text_note}\n Продажа: {date_last_sale}</a>"

        await message.answer(text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

        os.remove('images/' + f'{file.file_unique_id}.png')
        return

    os.remove('images/' + f'{file.file_unique_id}.png')


@main_router.message(F.text.casefold() == 'есть')
async def get_memo(message: Message, bot: Bot):
    file = await bot.get_file(message.reply_to_message.photo[-1].file_id)

    save_path = 'images'

    file_path = os.path.join(save_path, f'{file.file_unique_id}.png')

    await bot.download_file(file.file_path, destination=file_path)

    image = Image.open(f"images/{file.file_unique_id}.png")

    pytesseract.pytesseract.tesseract_cmd = 'Tesseract-OCR/tesseract.exe'
    text = pytesseract.image_to_string(image, lang='rus')

    pattern = r"Артикул:\s*(\d+)"
    match = re.search(pattern, text)

    if match:
        os.remove('images/' + f'{file.file_unique_id}.png')
        return ParsingIDriver().requesting_data_for_updating_the_notes(match.group(1))

    pattern = r"Арт:\s*(\d+)"

    matches = re.findall(pattern, text)

    if matches:
        os.remove('images/' + f'{file.file_unique_id}.png')
        return ParsingIDriver().requesting_data_for_updating_the_notes(matches[0])

    os.remove('images/' + f'{file.file_unique_id}.png')
