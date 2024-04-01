from .database import db
from .admin import add_user
from .translate.settings import settings
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


START_TEXT = """**Hello {} 😌
I am a google translator telegram bot.**

>> `I can translate from any languages to any languages.`

Made by @FayasNoushad"""

HELP_TEXT = """**Hey, Follow these steps:**

- Send /set or /settings for set a translate language 
- Send /reset for resetting current translate language
- Send /list or /languages for languages list
- Just send a text for translation 
- Add me your group and send /tr or /translate command for translation in group

**Available Commands**

/start - Checking bot online
/help - For more help
/about - For more about me
/status - For bot status
/list - For language list
/set - For set translate language
/reset - For reset translate language

Made by @FayasNoushad"""

ABOUT_TEXT = """--**About Me 😎**--

🤖 **Name :** [Translator Bot](https://telegram.me/{})

👨‍💻 **Developer :** [GitHub](https://github.com/FayasNoushad) | [Telegram](https://telegram.me/FayasNoushad)

🌐 **Source :** [👉 Click here](https://github.com/FayasNoushad/Translator-Bot-V3)

📝 **Language :** [Python3](https://python.org)

🧰 **Framework :** [Pyrogram](https://pyrogram.org)"""


START_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('⚙ Help', callback_data='help'),
            InlineKeyboardButton('About 🔰', callback_data='about'),
            InlineKeyboardButton('Close ✖️', callback_data='close')
        ]
    ]
)

HELP_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('🏘 Home', callback_data='home'),
            InlineKeyboardButton('About 🔰', callback_data='about'),
            InlineKeyboardButton('Close ✖️', callback_data='close')
        ]
    ]
)

ABOUT_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('🏘 Home', callback_data='home'),
            InlineKeyboardButton('Help ⚙', callback_data='help'),
            InlineKeyboardButton('Close ✖️', callback_data='close')
        ]
    ]
)

CLOSE_BUTTON = InlineKeyboardMarkup([[InlineKeyboardButton('Close', callback_data='close')]])


@Client.on_message(filters.private & filters.command(["start"]))
async def start(bot, message, cb=False):
    await add_user(message.from_user.id)
    if cb or (message and message.text and (message.text == "/start")):
        text = START_TEXT.format(message.from_user.mention)
        buttons = START_BUTTONS
        if cb:
            await message.message.edit_text(
                text=text,
                reply_markup=buttons,
                disable_web_page_preview=True
            )
            return
        await message.reply_text(
            text=text,
            disable_web_page_preview=True,
            reply_markup=buttons,
            quote=True
        )
    else:
        command = message.text.split(" ", 1)[1]
        if command == "set":
            await settings(bot, message)


@Client.on_message(filters.private & filters.command(["help"]))
async def help(bot, message, cb=False):
    await add_user(message.from_user.id)
    if cb:
        await message.message.edit_text(
            text=HELP_TEXT,
            reply_markup=HELP_BUTTONS,
            disable_web_page_preview=True
        )
    else:
        await message.reply_text(
            text=HELP_TEXT,
            reply_markup=HELP_BUTTONS,
            disable_web_page_preview=True,
            quote=True
        )


@Client.on_message(filters.private & filters.command(["about"]))
async def about(bot, message, cb=False):
    await add_user(message.from_user.id)
    text = ABOUT_TEXT.format((await bot.get_me()).username)
    if cb:
        await message.message.edit_text(
            text=text,
            reply_markup=ABOUT_BUTTONS,
            disable_web_page_preview=True
        )
    else:
        await message.reply_text(
            text=text,
            reply_markup=ABOUT_BUTTONS,
            disable_web_page_preview=True,
            quote=True
        )