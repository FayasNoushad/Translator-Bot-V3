# Author: Fayas (https://github.com/FayasNoushad) (@FayasNoushad)

import os
from ..vars import DEFAULT_LANGUAGE
from ..admin import db
from io import BytesIO
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from googletrans import Translator


BUTTONS = InlineKeyboardMarkup(
    [[InlineKeyboardButton('⚙ Feedback ⚙', url='https://telegram.me/FayasNoushad')]]
)

@Client.on_message(filters.group & filters.command(["tr", "translate"]))
async def command_filter(bot, update):
    if update.reply_to_message:
        if update.reply_to_message.text:
            text = update.reply_to_message.text
        elif update.reply_to_message.caption:
            text = update.reply_to_message.caption
        else:
            return 
    else:
        if update.text:
            text = update.text.split(" ", 1)[1]
        elif update.caption:
            text = update.caption.split(" ", 1)[1]
        else:
            return
    await translate(bot, update, text)


@Client.on_message(filters.private & (filters.text | filters.caption))
async def get_message(_, message):
    text = message.text if message.text else message.caption
    await translate(message, text)


async def translate(update, text):
    await update.reply_chat_action(enums.ChatAction.TYPING)
    message = await update.reply_text("`Translating...`", quote=True)
    try:
        language = await db.get_lang(update.from_user.id)
    except:
        language = DEFAULT_LANGUAGE
    translator = Translator()
    try:
        translate = translator.translate(text, dest=language)
        translate_text = f"**Translated to {language}**"
        translate_text += f"\n\n`{translate.text}`"
        if len(translate_text) < 4096:
            await message.edit_text(
                text=translate_text,
                disable_web_page_preview=True,
                reply_markup=BUTTONS
            )
        else:
            with BytesIO(str.encode(str(translate_text))) as translate_file:
                translate_file.name = language + ".txt"
                await update.reply_document(
                    document=translate_file,
                    quote=True,
                    reply_markup=BUTTONS
                )
                await message.delete()
                try:
                    os.remove(translate_file)
                except:
                    pass
    except Exception as error:
        print(error)
        await message.edit_text("Something wrong. Contact developer.")
        return
