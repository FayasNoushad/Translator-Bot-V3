from .database import db
from .admin import add_user
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup
from .commands import start, help, about
from googletrans.constants import LANGUAGES
from .translate.settings import language_buttons, SETTINGS_TEXT


@Client.on_callback_query()
async def cb_data(_, message):
    await add_user(message.from_user.id)
    if message.data == "home":
        await start(_, message, cb=True)
    elif message.data == "help":
        await help(_, message, cb=True)
    elif message.data == "about":
        await about(_, message, cb=True)
    elif message.data == "close":
        await message.message.delete()
    elif message.data.startswith("page+"):
        await message.answer("Processing")
        page_no = int(message.data.split("+")[1]) - 1
        await message.message.edit_reply_markup(
            InlineKeyboardMarkup(
                language_buttons()[page_no]
            )
        )
    elif message.data.startswith("set+"):
        try:
            language = message.data.split("+")[1]
            await db.update_lang(message.from_user.id, language)
            lang_text = f"{LANGUAGES[language].capitalize()} ({language})"
            await message.message.edit_text(
                text=SETTINGS_TEXT.format(await db.get_lang(message.from_user.id)),
                disable_web_page_preview=True,
                reply_markup=message.message.reply_markup
            )
            alert_text = f"Language changed to {language}"
            await message.answer(text=alert_text, show_alert=True)
        except Exception as error:
            if 'MESSAGE_NOT_MODIFIED' in str(error):
                return
            print(error)
            await message.message.edit_text("Something wrong.")
