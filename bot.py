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

from google import genai


# =========================================================
# CONFIG
# =========================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set!")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set!")


# Gemini client
gemini_client = genai.Client(
    api_key=GEMINI_API_KEY
)

# Gemini model
GEMINI_MODEL = "gemini-3.6-flash"


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
# START
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
# HELP
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
# AI CHAT PLACEHOLDER
# =========================================================

@dp.callback_query(F.data == "ai")
async def ai_button(callback: CallbackQuery):

    await callback.message.answer(
        "🤖 *AI Chat*\n\n"
        "AI Chat ကို နောက်အဆင့်မှာ Gemini နဲ့ "
        "ချိတ်ပေးမယ်။",
        parse_mode="Markdown",
    )

    await callback.answer()


# =========================================================
# TRANSLATOR MENU
# =========================================================

@dp.callback_query(F.data == "translate")
async def translate_button(callback: CallbackQuery):

    await callback.message.answer(
        "🌐 *Auto Translator*\n\n"
        "ဘာသာပြန်ချင်တဲ့စာကို ပို့ပါ 👇\n\n"
        "🤖 Bot က မူရင်းဘာသာစကားကို "
        "အလိုအလျောက်သိပါမယ်။\n\n"
        "🇲🇲 မြန်မာ\n"
        "🇬🇧 English\n"
        "🇹🇭 Thai\n"
        "🇨🇳 Chinese\n"
        "🌍 အခြားဘာသာစကားများ\n\n"
        "📌 မူရင်းဘာသာစကားနဲ့ "
        "ဘာသာပြန်လိုတဲ့ဘာသာစကားကို "
        "စာထဲမှာပြောနိုင်ပါတယ်။\n\n"
        "ဥပမာ:\n"
        "Translate to English: နေကောင်းလား",
        parse_mode="Markdown",
    )

    await callback.answer()


# =========================================================
# GEMINI TRANSLATION
# =========================================================

async def translate_with_gemini(text: str):

    prompt = f"""
You are a professional translator.

Translate the user's text accurately and naturally.

IMPORTANT RULES:
1. Detect the source language automatically.
2. If the user explicitly says "Translate to English", translate to English.
3. If the user explicitly says "Translate to Thai", translate to Thai.
4. If the user explicitly says "Translate to Chinese", translate to Chinese.
5. If the user explicitly says "Translate to Burmese" or "Myanmar", translate to Burmese.
6. If no target language is specified:
   - If the source is Burmese, translate to English.
   - If the source is English, translate to Burmese.
   - If the source is Thai, translate to Burmese.
   - If the source is Chinese, translate to Burmese.
   - For other languages, translate to Burmese.
7. Keep the original meaning.
8. Do not explain the translation.
9. Return ONLY the translated text.
10. Do not add quotation marks.

User text:
{text}
"""

    try:

        response = await asyncio.to_thread(
            gemini_client.models.generate_content,
            model=GEMINI_MODEL,
            contents=prompt
        )

        result = response.text

        if not result:
            return None

        return result.strip()

    except Exception as e:

        print(
            f"❌ Gemini translation error: {type(e).__name__}: {e}"
        )

        return None


# =========================================================
# TEXT MESSAGE HANDLER
# =========================================================

@dp.message(F.text)
async def translate_text(message: Message):

    text = message.text.strip()

    # Ignore commands
    if text.startswith("/"):
        return

    processing = await message.answer(
        "🌐 ဘာသာပြန်နေပါတယ်... ⏳"
    )

    result = await translate_with_gemini(text)

    if result:

        await processing.edit_text(
            "🌐 *Auto Translator*\n\n"
            f"📝 မူရင်းစာ:\n{text}\n\n"
            f"🔤 *ဘာသာပြန်ချက်:*\n{result}",
            parse_mode="Markdown",
        )

    else:

        await processing.edit_text(
            "❌ ဘာသာပြန်လို့ မရပါဘူး။\n\n"
            "Gemini API ကို စစ်ဆေးပေးပါ။"
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
        os.getenv("PORT", 8080)
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
# RUN
# =========================================================

if __name__ == "__main__":

    asyncio.run(main())
