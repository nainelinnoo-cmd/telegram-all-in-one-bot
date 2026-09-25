import os
import asyncio

from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)


# =========================================================
# BOT CONFIG
# =========================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# =========================================================
# MAIN MENU
# =========================================================

def main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🤖 AI Chat",
                    callback_data="ai"
                ),
                InlineKeyboardButton(
                    text="🌐 Translator",
                    callback_data="translate"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="📝 SRT Tools",
                    callback_data="srt"
                ),
                InlineKeyboardButton(
                    text="🎬 Video Tools",
                    callback_data="video"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🖼️ Image Tools",
                    callback_data="image"
                ),
                InlineKeyboardButton(
                    text="🎵 Music",
                    callback_data="music"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="📁 File Tools",
                    callback_data="file"
                ),
                InlineKeyboardButton(
                    text="⚙️ Settings",
                    callback_data="settings"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="ℹ️ Help",
                    callback_data="help"
                )
            ],
        ]
    )


# =========================================================
# /START
# =========================================================

@dp.message(CommandStart())
async def start(message: Message):
    name = message.from_user.first_name or "Friend"

    await message.answer(
        f"👋 မင်္ဂလာပါ {name}!\n\n"
        "🚀 *All-in-One Telegram Bot* မှ ကြိုဆိုပါတယ်။\n\n"
        "အောက်က Menu ကနေ လိုချင်တာကို ရွေးပါ 👇",
        reply_markup=main_menu(),
        parse_mode="Markdown",
    )


# =========================================================
# /HELP
# =========================================================

@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "ℹ️ *Help*\n\n"
        "/start — Main Menu\n"
        "/help — Help\n\n"
        "🤖 AI Chat\n"
        "🌐 Translation\n"
        "📝 Subtitle / SRT\n"
        "🎬 Video Tools\n"
        "🖼️ Image Tools\n"
        "🎵 Music Tools\n"
        "📁 File Tools",
        parse_mode="Markdown",
    )


# =========================================================
# AI CHAT
# =========================================================

@dp.callback_query(F.data == "ai")
async def ai_button(callback: CallbackQuery):

    await callback.message.answer(
        "🤖 *AI Chat*\n\n"
        "AI Chat feature ကို နောက်တစ်ဆင့်မှာ "
        "AI API နဲ့ ချိတ်ပေးမယ်။",
        parse_mode="Markdown",
    )

    await callback.answer()


# =========================================================
# TRANSLATOR
# =========================================================

@dp.callback_query(F.data == "translate")
async def translate_button(callback: CallbackQuery):

    await callback.message.answer(
        "🌐 *Translator*\n\n"
        "ဘာသာပြန်ချင်တဲ့စာကို ဒီမှာပို့ပါ။ 👇\n\n"
        "ဥပမာ:\n"
        "Hello, how are you?\n\n"
        "🇬🇧 English → 🇲🇲 Myanmar\n"
        "🇲🇲 Myanmar → 🇬🇧 English\n\n"
        "💡 Translation API ကို နောက်အဆင့်မှာ "
        "ချိတ်ပေးမယ်။",
        parse_mode="Markdown",
    )

    await callback.answer()


# =========================================================
# TRANSLATOR TEXT RECEIVER
# =========================================================

@dp.message(F.text)
async def translate_text(message: Message):

    text = message.text

    # Commands ကို Translator မလုပ်စေဖို့
    if text.startswith("/"):
        return

    await message.answer(
        "🌐 *Translator*\n\n"
        "📝 မူရင်းစာ:\n"
        f"{text}\n\n"
        "🚧 ဒီစာကို လက်ခံရရှိပါပြီ။\n\n"
        "🔧 Translation API ကို နောက်အဆင့်မှာ "
        "ချိတ်ပြီး တကယ်ဘာသာပြန်ပေးမယ်။",
        parse_mode="Markdown",
    )


# =========================================================
# OTHER MENU BUTTONS
# =========================================================

@dp.callback_query()
async def menu_buttons(callback: CallbackQuery):

    names = {
        "srt": "📝 SRT Tools",
        "video": "🎬 Video Tools",
        "image": "🖼️ Image Tools",
        "music": "🎵 Music Tools",
        "file": "📁 File Tools",
        "settings": "⚙️ Settings",
        "help": "ℹ️ Help",
    }

    name = names.get(callback.data)

    if name:

        await callback.message.answer(
            f"{name}\n\n"
            "🚧 ဒီ Feature ကို နောက်တစ်ဆင့်မှာ "
            "ထည့်ပေးမယ်။"
        )

    await callback.answer()


# =========================================================
# RENDER HEALTH CHECK
# =========================================================

async def health(request):

    return web.Response(
        text="Bot is running! 🤖"
    )


async def start_web_server():

    app = web.Application()

    app.router.add_get(
        "/",
        health
    )

    runner = web.AppRunner(app)

    await runner.setup()

    port = int(
        os.getenv(
            "PORT",
            8080
        )
    )

    site = web.TCPSite(
        runner,
        "0.0.0.0",
        port
    )

    await site.start()

    print(
        f"🌐 Web server running on port {port}"
    )


# =========================================================
# MAIN
# =========================================================

async def main():

    print("🤖 Bot is starting...")

    await start_web_server()

    print("✅ Web server started")

    print("🚀 Telegram bot polling started")

    await dp.start_polling(bot)


# =========================================================
# RUN BOT
# =========================================================

if __name__ == "__main__":

    asyncio.run(main())
