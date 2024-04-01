from googletrans import constants
from .translate import BUTTONS
from pyrogram import Client, filters


@Client.on_message(filters.command(["list", "languages", "langs", "languages_list"]))
async def languages_list(bot, message):
    languages = constants.LANGUAGES
    languages_text = "**Languages**\n"
    for language in languages:
        languages_text += f"\n`{languages[language].capitalize()}` -> `{language}`"
    await message.reply_text(
        text=languages_text,
        disable_web_page_preview=True,
        reply_markup=BUTTONS,
        quote=True
    )