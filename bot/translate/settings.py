from ..database import db
from ..admin import add_user
from ..vars import DEFAULT_LANGUAGE
from googletrans.constants import LANGUAGES
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def language_buttons():
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


SETTINGS_TEXT = "Select your language for translating. Current default language is `{}`."
SETTINGS_BUTTONS = InlineKeyboardMarkup(
    language_buttons()[0]
)


@Client.on_message(filters.command(["set", "settings"]))
async def settings(bot, message):
    if message.chat.type != enums.ChatType.PRIVATE:
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
        await message.reply_text(
            text="Set your language via private",
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            quote=True
        )
        return
    await add_user(message.from_user.id)
    await message.reply_text(
        text=SETTINGS_TEXT.format(await db.get_lang(message.from_user.id)),
        disable_web_page_preview=True,
        reply_markup=SETTINGS_BUTTONS,
        quote=True
    )


@Client.on_message(filters.private & filters.command(["reset", "unset"]))
async def reset(bot, message):
    await add_user(message.from_user.id)
    await db.update_lang(message.from_user.id, DEFAULT_LANGUAGE)
    await message.reply_text(
        text="Language reset successfully",
        disable_web_page_preview=True,
        quote=True
    )
