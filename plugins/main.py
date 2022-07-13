# Author: Fayas (https://github.com/FayasNoushad) (@FayasNoushad)

import os
from .vars import DATABASE, DEFAULT_LANGUAGE
from .admin import Database
from io import BytesIO
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from googletrans import Translator, constants


START_TEXT = """**Hello {} 😌
I am a google translator telegram bot.**

>> `I can translate from any languages to any languages.`

Made by @FayasNoushad"""

HELP_TEXT = """**Hey, Follow these steps:**

- Send /set or /settings for set a default language 
- Send /unset for unsetting current default language
- Send /list or /languages for languages list
- Just send a text for translation 
- Add me your group and send /tr or /translate command for translation in group

**Available Commands**

/start - Checking bot online
/help - For more help
/about - For more about me
/status - For bot status
/list - For language list
/set - For set default language
/unset - For unset default language

Made by @FayasNoushad"""

ABOUT_TEXT = """--**About Me 😎**--

🤖 **Name :** [Translator Bot](https://telegram.me/{})

👨‍💻 **Developer :** [Fayas](https://github.com/FayasNoushad)

📢 **Channel :** [Fayas Noushad](https://telegram.me/FayasNoushad)

🌐 **Source :** [👉 Click here](https://github.com/FayasNoushad/Translator-Bot-V3)

📝 **Language :** [Python3](https://python.org)

🧰 **Framework :** [Pyrogram](https://pyrogram.org)

📡 **Server :** [Heroku](https://heroku.com)"""

SETTINGS_TEXT = "Select your language for translating. Current default language is `{}`."

BUTTONS = [InlineKeyboardButton('⚙ Join Updates Channel ⚙', url='https://telegram.me/FayasNoushad')]

db = Database(DATABASE)

LANGUAGES = constants.LANGUAGES

LANGUAGES_TEXT = "**Languages**\n"
for language in LANGUAGES:
    LANGUAGES_TEXT += f"\n`{LANGUAGES[language].capitalize()}` -> `{language}`"


def Language_buttons():
    pages = []
    button_limit = 2
    line_limit = 8
    for language in LANGUAGES:
        button = InlineKeyboardButton(text=LANGUAGES[language].capitalize(), callback_data="set+"+language)
        if len(pages) == 0 or len(pages[-1]) >= line_limit and len(pages[-1][-1]) >= button_limit:
            pages.append([[button]])
        elif len(pages[-1]) == 0 or len(pages[-1][-1]) >= button_limit:
            pages[-1].append([button])
        else:
            pages[-1][-1].append(button)
    page_no = 0
    no_buttons = []
    if len(pages) == 1:
        return pages
    for page in pages:
        page_no += 1
        page_buttons = []
        if page == pages[0]:
            page_buttons.append(
                InlineKeyboardButton(
                    text="-->",
                    callback_data="page+"+str(page_no+1)
                )
            )
        elif page == pages[-1]:
            page_buttons.append(
                InlineKeyboardButton(
                    text="<--",
                    callback_data="page+"+str(page_no-1)
                )
            )
        else:
            page_buttons.append(
                InlineKeyboardButton(
                    text="<--",
                    callback_data="page+"+str(page_no-1)
                )
            )
            page_buttons.append(
                InlineKeyboardButton(
                    text="-->",
                    callback_data="page+"+str(page_no+1)
                )
            )
        pages[page_no-1].append(page_buttons)
        no_buttons.append(
            InlineKeyboardButton(
                text=str(page_no),
                callback_data="page+"+str(page_no)
            )
        )
        pages[page_no-1].append(no_buttons)
    return pages


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

SETTINGS_BUTTONS = InlineKeyboardMarkup(
        Language_buttons()[0]
    )

CLOSE_BUTTON = InlineKeyboardMarkup([[InlineKeyboardButton('Close', callback_data='close')]])

TRANSLATE_BUTTON = InlineKeyboardMarkup([BUTTONS])


@Client.on_callback_query()
async def cb_data(bot, update):
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            disable_web_page_preview=True,
            reply_markup=HELP_BUTTONS
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT.format((await bot.get_me()).username),
            disable_web_page_preview=True,
            reply_markup=ABOUT_BUTTONS
        )
    elif update.data == "close":
        await update.message.delete()
    elif update.data.startswith("page+"):
        await update.answer("Processing")
        page_no = int(update.data.split("+")[1]) - 1
        await update.message.edit_reply_markup(
            InlineKeyboardMarkup(
                Language_buttons()[page_no]
            )
        )
    elif update.data.startswith("set+"):
        language = update.data.split("+")[1]
        await db.update_lang(update.from_user.id, language)
        await update.message.edit_text(
             text=SETTINGS_TEXT.format(await db.get_lang(update.from_user.id)),
             disable_web_page_preview=True,
             reply_markup=update.message.reply_markup
        )
        alert_text = f"Language changed to {language}"
        await update.answer(text=alert_text, show_alert=True)


@Client.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
    if update.text == "/start":
        text = START_TEXT.format(update.from_user.mention)
        reply_markup = START_BUTTONS
        await update.reply_text(
            text=text,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            quote=True
        )
    else:
        command = update.text.split(" ", 1)[1]
        if command == "set":
            await settings(bot, update)


@Client.on_message(filters.private & filters.command(["help"]))
async def help(bot, update):
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
    await update.reply_text(
        text=HELP_TEXT,
        disable_web_page_preview=True,
        reply_markup=HELP_BUTTONS,
        quote=True
    )


@Client.on_message(filters.private & filters.command(["about"]))
async def about(bot, update):
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
    await update.reply_text(
        text=ABOUT_TEXT.format((await bot.get_me()).username),
        disable_web_page_preview=True,
        reply_markup=ABOUT_BUTTONS,
        quote=True
    )


@Client.on_message(filters.command(["set", "settings"]))
async def settings(bot, update):
    if update.chat.type != "PRIVATE":
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Click here",
                        url=f"https://telegram.me/{(await bot.get_me()).username}?start=set"
                    )
                ]
            ]
        )
        await update.reply_text(
            text="Set your language via private",
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            quote=True
        )
        return
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
    await update.reply_text(
        text=SETTINGS_TEXT.format(await db.get_lang(update.from_user.id)),
        disable_web_page_preview=True,
        reply_markup=SETTINGS_BUTTONS,
        quote=True
    )


@Client.on_message(filters.private & filters.command(["unset"]))
async def unset(bot, update):
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
    await db.update_lang(update.from_user.id, DEFAULT_LANGUAGE)
    await update.reply_text(
        text="Language unset successfully",
        disable_web_page_preview=True,
        quote=True
    )


@Client.on_message(filters.private & filters.command(["languages", "list"]))
async def languages(bot, update):
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
    await update.reply_text(
        text=LANGUAGES_TEXT,
        disable_web_page_preview=True,
        reply_markup=TRANSLATE_BUTTON,
        quote=True
    )


@Client.on_message(filters.private & filters.command("status"))
async def status(bot, update):
    total_users = await db.total_users_count()
    text = "**Bot Status**\n"
    text += f"\n**Total Users:** `{total_users}`"
    await update.reply_text(
        text=text,
        quote=True,
        disable_web_page_preview=True
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
    message = await update.reply_text("`Translating...`")
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
                disable_web_page_preview=True
            )
        else:
            with BytesIO(str.encode(str(translate_text))) as translate_file:
                translate_file.name = language + ".txt"
                await update.reply_document(
                    document=translate_file
                )
                await message.delete()
                try:
                    os.remove(translate_file)
                except:
                    pass
    except Exception as error:
        print(error)
        await message.edit_text("Something wrong. Contact @TheFayas.")
        return
