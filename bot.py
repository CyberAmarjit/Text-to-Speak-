import os
import time
import logging
import tempfile
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from gtts import gTTS
from pydub import AudioSegment

# === BOT TOKEN ===
BOT_TOKEN = "YOUR TELEGRAM BOT TOKEN"

# === LOGGING ===
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# === USER SETTINGS ===
user_settings = {}

# === /start ===
def start(update: Update, context: CallbackContext):
    msg = (
        "🎧 *Welcome to JARVIS Voice Bot!*\n\n"
        "Send any text and I’ll convert it to voice.\n\n"
        "✨ *Commands:*\n"
        "• /setlang hi|en → Choose language\n"
        "• /speed normal|slow → Set voice speed\n"
        "• /format mp3|ogg → Choose format\n"
        "• /voice male|female → Choose voice type\n"
        "• /music on|off → Background music toggle\n"
        "• /help → Show all commands again"
    )
    update.message.reply_text(msg, parse_mode="Markdown")

def help_command(update: Update, context: CallbackContext):
    start(update, context)

# === SETTINGS COMMANDS ===
def set_language(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if len(context.args) == 0:
        update.message.reply_text("🗣️ Usage: /setlang hi or /setlang en")
        return
    lang = context.args[0].lower()
    if lang not in ["hi", "en"]:
        update.message.reply_text("⚠️ Only 'hi' or 'en' allowed.")
        return
    user_settings.setdefault(user_id, {})["lang"] = lang
    update.message.reply_text(f"✅ Language set to: {lang.upper()}")

def set_speed(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if len(context.args) == 0:
        update.message.reply_text("🐢 Usage: /speed normal or /speed slow")
        return
    speed = context.args[0].lower()
    if speed not in ["normal", "slow"]:
        update.message.reply_text("⚠️ Only 'normal' or 'slow' allowed.")
        return
    user_settings.setdefault(user_id, {})["speed"] = speed
    update.message.reply_text(f"✅ Voice speed set to: {speed.capitalize()}")

def set_format(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if len(context.args) == 0:
        update.message.reply_text("🎧 Usage: /format mp3 or ogg")
        return
    fmt = context.args[0].lower()
    if fmt not in ["mp3", "ogg"]:
        update.message.reply_text("⚠️ Only 'mp3' or 'ogg' allowed.")
        return
    user_settings.setdefault(user_id, {})["format"] = fmt
    update.message.reply_text(f"✅ Audio format set to: {fmt.upper()}")

def set_voice(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if len(context.args) == 0:
        update.message.reply_text("🎙️ Usage: /voice male or female")
        return
    voice = context.args[0].lower()
    if voice not in ["male", "female"]:
        update.message.reply_text("⚠️ Only 'male' or 'female' allowed.")
        return
    user_settings.setdefault(user_id, {})["voice"] = voice
    update.message.reply_text(f"✅ Voice style set to: {voice.capitalize()}")

def set_music(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if len(context.args) == 0:
        update.message.reply_text("🎵 Usage: /music on or off")
        return
    state = context.args[0].lower()
    if state not in ["on", "off"]:
        update.message.reply_text("⚠️ Only 'on' or 'off' allowed.")
        return
    user_settings.setdefault(user_id, {})["music"] = state
    update.message.reply_text(f"🎶 Background music turned {state.upper()}")

# === TEXT TO VOICE ===
def text_to_voice(update: Update, context: CallbackContext):
    user_text = update.message.text.strip()
    user_id = update.message.from_user.id
    settings = user_settings.get(user_id, {"lang": None, "speed": "normal", "format": "mp3", "voice": "female", "music": "off"})

    if not user_text:
        update.message.reply_text("⚠️ Please send some text.")
        return

    msg = update.message.reply_text("🎤 Generating premium voice...")

    try:
        # Auto language detect
        lang = settings["lang"] or ("hi" if any("\u0900" <= ch <= "\u097F" for ch in user_text) else "en")
        slow = True if settings.get("speed") == "slow" else False
        fmt = settings.get("format", "mp3")

        # Voice style effect (simple pitch trick)
        voice_style = settings.get("voice", "female")
        pitch_shift = -3 if voice_style == "male" else 3

        # Generate TTS audio
        tts = gTTS(text=user_text, lang=lang, slow=slow)
        temp_voice = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_voice.name)
        temp_voice.close()

        voice_audio = AudioSegment.from_file(temp_voice.name)

        # Adjust pitch for male/female
        voice_audio = voice_audio._spawn(voice_audio.raw_data, overrides={
            "frame_rate": int(voice_audio.frame_rate * (0.9 if voice_style == "male" else 1.1))
        }).set_frame_rate(44100)

        # Add background music if enabled
        if settings.get("music") == "on":
            bg_music = AudioSegment.silent(duration=len(voice_audio))
            music_path = os.path.join(os.path.dirname(__file__), "bg.mp3")
            if os.path.exists(music_path):
                bg_music = AudioSegment.from_file(music_path).apply_gain(-10)
                if len(bg_music) < len(voice_audio):
                    bg_music = bg_music * (len(voice_audio) // len(bg_music) + 1)
            mixed = bg_music.overlay(voice_audio)
            voice_audio = mixed

        # Save final output
        temp_final = tempfile.NamedTemporaryFile(delete=False, suffix=f".{fmt}")
        voice_audio.export(temp_final.name, format=fmt)
        temp_final.close()

        with open(temp_final.name, "rb") as audio:
            update.message.reply_audio(
                audio=audio,
                caption=f"✅ *Voice Ready!*\n👤 Voice: `{voice_style}`\n🎧 Music: `{settings['music']}`\n🌐 Lang: `{lang}`",
                parse_mode="Markdown"
            )

        os.unlink(temp_voice.name)
        os.unlink(temp_final.name)

    except Exception as e:
        logging.error(f"Error: {e}")
        update.message.reply_text("❌ Error aaya hai, phir se try karein!")
    finally:
        try:
            msg.delete()
        except:
            pass

# === MAIN ===
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("setlang", set_language))
    dp.add_handler(CommandHandler("speed", set_speed))
    dp.add_handler(CommandHandler("format", set_format))
    dp.add_handler(CommandHandler("voice", set_voice))
    dp.add_handler(CommandHandler("music", set_music))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, text_to_voice))

    print("🚀 Premium Voice Bot Running...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
