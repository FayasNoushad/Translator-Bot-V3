from .database import db
from .admin import add_user
from pyrogram import Client, filters


@Client.on_message(filters.private & filters.command(["status", "bot_status"]))
async def status(bot, message):
    await add_user(message.from_user.id)
    total_users = await db.total_users_count()
    text = "**Bot Status**\n"
    text += f"\n**Total Users:** `{total_users}`"
    await message.reply_text(
        text=text,
        quote=True,
        disable_web_page_preview=True
    )