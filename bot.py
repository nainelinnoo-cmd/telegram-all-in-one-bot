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

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


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


@dp.callback_query(F.data == "ai")
async def ai_button(callback: CallbackQuery):
    await callback.message.answer(
        "🤖 *AI Chat*\n\n"
        "AI Chat feature ကို နောက်တစ်ဆင့်မှာ API နဲ့ ချိတ်ပေးမယ်။",
        parse_mode="Markdown",
    )
    await callback.answer()


@dp.callback_query()
async def menu_buttons(callback: CallbackQuery):
    names = {
        "translate": "🌐 Translator",
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
            "🚧 ဒီ Feature ကို နောက်တစ်ဆင့်မှာ ထည့်ပေးမယ်။"
        )

    await callback.answer()


async def health(request):
    return web.Response(text="Bot is running! 🤖")


async def start_web_server():
    app = web.Application()
    app.router.add_get("/", health)

    runner = web.AppRunner(app)
    await runner.setup()

    port = int(os.getenv("PORT", 8080))

    site = web.TCPSite(
        runner,
        "0.0.0.0",
        port
    )

    await site.start()

    print(f"🌐 Web server running on port {port}")


async def main():
    print("🤖 Bot is starting...")

    await start_web_server()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
