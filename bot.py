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


# =========================================================
# GEMINI
# =========================================================

gemini_client = genai.Client(
    api_key=GEMINI_API_KEY
)

# Gemini model
GEMINI_MODEL = "gemini-3.8-flash"


# =========================================================
# TELEGRAM
# =========================================================

bot = Bot(
    token=BOT_TOKEN
)

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
# AI CHAT
# =========================================================

@dp.callback_query(F.data == "ai")
async def ai_button(callback: CallbackQuery):

    await callback.message.answer(
        "🤖 *AI Chat*\n\n"
        "AI Chat ကို နောက်အဆင့်မှာ "
        "Gemini နဲ့ ချိတ်ပေးမယ်။",
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
        "🇲🇲 မြန်မာ → 🇬🇧 English\n"
        "🇬🇧 English → 🇲🇲 မြန်မာ\n"
        "🇹🇭 Thai → 🇲🇲 မြန်မာ\n"
        "🇨🇳 Chinese → 🇲🇲 မြန်မာ\n\n"
        "🌍 အခြားဘာသာစကားတွေလည်း ရပါတယ်။\n\n"
        "📌 Target language သတ်မှတ်ချင်ရင်:\n"
        "*Translate to English: နေကောင်းလား*",
        parse_mode="Markdown",
    )

    await callback.answer()


# =========================================================
# GEMINI TRANSLATOR
# =========================================================

async def translate_text_with_gemini(text: str):

    prompt = f"""
You are a professional translation assistant.

Your job is to translate the user's message.

RULES:

1. Detect the source language automatically.

2. If the user explicitly requests a target language,
   translate into that language.

3. Examples of target language requests:
   - Translate to English
   - Translate to Burmese
   - Translate to Myanmar
   - Translate to Thai
   - Translate to Chinese
   - Translate to Japanese
   - Translate to Korean

4. If the user does NOT specify a target language:
   - Burmese → English
   - English → Burmese
   - Thai → Burmese
   - Chinese → Burmese
   - Japanese → Burmese
   - Korean → Burmese
   - Other languages → Burmese

5. Preserve the original meaning.

6. Make the translation natural and easy to understand.

7. Do not explain anything.

8. Do not add notes.

9. Do not add quotation marks.

10. Return ONLY the translated text.

USER MESSAGE:
{text}
"""

    try:

        response = await asyncio.to_thread(
            gemini_client.models.generate_content,
            model=GEMINI_MODEL,
            contents=prompt
        )

        if not response:
            return None

        result = response.text

        if not result:
            return None

        return result.strip()

    except Exception as e:

        print(
            "❌ GEMINI TRANSLATION ERROR:"
        )

        print(
            type(e).__name__,
            str(e)
        )

        return None


# =========================================================
# TEXT MESSAGE
# =========================================================

@dp.message(F.text)
async def text_message(message: Message):

    text = message.text.strip()

    # Ignore commands
    if text.startswith("/"):
        return

    processing = await message.answer(
        "🌐 ဘာသာပြန်နေပါတယ်... ⏳"
    )

    result = await translate_text_with_gemini(
        text
    )

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

    name = names.get(
        callback.data
    )

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

    runner = web.AppRunner(
        app
    )

    await runner.setup()

    port = int(
        os.getenv(
            "PORT",
            "8080"
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

    print(
        "🤖 Bot is starting..."
    )

    await start_web_server()

    print(
        "✅ Web server started"
    )

    print(
        "🚀 Telegram bot polling started"
    )

    await dp.start_polling(
        bot
    )


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    asyncio.run(
        main()
    )
