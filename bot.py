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

from deep_translator import GoogleTranslator


# =========================================================
# CONFIG
# =========================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set!")


# =========================================================
# TELEGRAM
# =========================================================

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
                ),
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
        "🚧 AI Chat ကို နောက်တစ်ဆင့်မှာ "
        "ထည့်ပေးမယ်။",
        parse_mode="Markdown",
    )

    await callback.answer()


# =========================================================
# TRANSLATOR MENU
# =========================================================

@dp.callback_query(F.data == "translate")
async def translate_button(callback: CallbackQuery):

    await callback.message.answer(
        "🌐 *Fast Translator*\n\n"
        "ဘာသာပြန်ချင်တဲ့စာကို တိုက်ရိုက်ပို့ပါ 👇\n\n"
        "🔄 Auto mode:\n"
        "🇲🇲 မြန်မာ → 🇬🇧 English\n"
        "🇬🇧 English → 🇲🇲 မြန်မာ\n"
        "🇹🇭 Thai → 🇲🇲 မြန်မာ\n"
        "🇨🇳 Chinese → 🇲🇲 မြန်မာ\n"
        "🇯🇵 Japanese → 🇲🇲 မြန်မာ\n"
        "🇰🇷 Korean → 🇲🇲 မြန်မာ\n\n"
        "🎯 Target language သတ်မှတ်ချင်ရင်:\n"
        "`Translate to English: နေကောင်းလား`\n\n"
        "`Translate to Thai: မင်္ဂလာပါ`",
        parse_mode="Markdown",
    )

    await callback.answer()


# =========================================================
# LANGUAGE MAP
# =========================================================

LANGUAGE_CODES = {
    "english": "en",
    "eng": "en",
    "en": "en",

    "burmese": "my",
    "myanmar": "my",
    "မြန်မာ": "my",
    "မြန်မာစာ": "my",
    "my": "my",

    "thai": "th",
    "ထိုင်း": "th",
    "th": "th",

    "chinese": "zh-CN",
    "china": "zh-CN",
    "တရုတ်": "zh-CN",
    "zh": "zh-CN",

    "japanese": "ja",
    "japan": "ja",
    "ဂျပန်": "ja",
    "ja": "ja",

    "korean": "ko",
    "korea": "ko",
    "ကိုရီးယား": "ko",
    "ko": "ko",

    "french": "fr",
    "fr": "fr",

    "german": "de",
    "de": "de",

    "spanish": "es",
    "es": "es",

    "italian": "it",
    "it": "it",

    "russian": "ru",
    "ru": "ru",

    "vietnamese": "vi",
    "vi": "vi",

    "indonesian": "id",
    "id": "id",

    "malay": "ms",
    "ms": "ms",

    "hindi": "hi",
    "hi": "hi",
}


# =========================================================
# PARSE TARGET LANGUAGE
# =========================================================

def parse_translation_request(text: str):

    lower = text.lower().strip()

    prefixes = [
        "translate to ",
        "translate into ",
        "translation to ",
    ]

    for prefix in prefixes:

        if lower.startswith(prefix):

            remaining = text[len(prefix):].strip()

            if ":" not in remaining:
                return None, text

            language_part, original_text = (
                remaining.split(":", 1)
            )

            language_part = (
                language_part.strip()
                .lower()
            )

            original_text = (
                original_text.strip()
            )

            target = LANGUAGE_CODES.get(
                language_part
            )

            if target and original_text:
                return target, original_text

    return None, text


# =========================================================
# FAST TRANSLATOR
# =========================================================

async def translate_text(text: str):

    target_language, original_text = (
        parse_translation_request(text)
    )

    # -----------------------------------------------------
    # AUTO TARGET
    # -----------------------------------------------------

    if not target_language:

        # Detect source language
        detected = await asyncio.to_thread(
            GoogleTranslator(
                source="auto",
                target="en"
            ).translate,
            original_text
        )

        # We don't use the translated result here.
        # Instead, GoogleTranslator's auto detection
        # is used again below with the selected target.

        # Simple Burmese detection
        if any(
            "\u1000" <= char <= "\u109f"
            for char in original_text
        ):
            target_language = "en"

        # Thai
        elif any(
            "\u0e00" <= char <= "\u0e7f"
            for char in original_text
        ):
            target_language = "my"

        else:
            # English / other Latin languages
            target_language = "my"


    # -----------------------------------------------------
    # TRANSLATE
    # -----------------------------------------------------

    result = await asyncio.to_thread(
        GoogleTranslator(
            source="auto",
            target=target_language
        ).translate,
        original_text
    )

    if not result:
        raise RuntimeError(
            "Empty translation result"
        )

    return result


# =========================================================
# TEXT MESSAGE HANDLER
# =========================================================

@dp.message(F.text)
async def text_message(message: Message):

    text = message.text.strip()

    # Ignore Telegram commands
    if text.startswith("/"):
        return

    processing = await message.answer(
        "🌐 ဘာသာပြန်နေပါတယ်... ⚡"
    )

    try:

        result = await translate_text(text)

        await processing.edit_text(
            "🌐 *Translation*\n\n"
            f"📝 {text}\n\n"
            f"🔤 *{result}*",
            parse_mode="Markdown",
        )

    except Exception as e:

        print(
            "❌ TRANSLATION ERROR:",
            str(e)
        )

        await processing.edit_text(
            "❌ ဘာသာပြန်လို့ မရသေးပါဘူး။\n\n"
            "ခဏနေပြီး ပြန်စမ်းကြည့်ပါ။"
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
