import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import yt_dlp

# 🔑 توکن ربات خودت رو اینجا قرار بده
BOT_TOKEN = "7920389849:AAF9y57ns7Nn1PCdP0mZqdI9_WVMK8GEF5U"

# پوشه ذخیره فایل‌ها (اگر نبود، بسازیم)
if not os.path.exists("downloads"):
    os.makedirs("downloads")

# 🎬 شروع کار بات
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! فایل یا لینک یوتیوب بفرست تا برات دانلود کنم 🎥")

# 📥 هندلر فایل‌های دریافتی
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    file = message.document or message.video or message.audio
    if file:
        telegram_file = await file.get_file()
        filename = f"./downloads/{file.file_name}"
        await telegram_file.download_to_drive(custom_path=filename)
        await message.reply_text(f"✅ فایل با موفقیت ذخیره شد: {file.file_name}")
    else:
        await message.reply_text("فایلی دریافت نشد ❌")

# 📥 هندلر لینک‌های یوتیوب
async def handle_youtube(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if "youtube.com" in url or "youtu.be" in url:
        await update.message.reply_text("⏳ در حال دانلود از یوتیوب...")
        try:
            ydl_opts = {
                'outtmpl': './downloads/%(title)s.%(ext)s',
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
                'quiet': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

            with open(filename, 'rb') as f:
                await update.message.reply_video(video=f, caption="✅ ویدیو آماده است")

        except Exception as e:
            await update.message.reply_text(f"❌ خطا در دانلود: {e}")
    else:
        await update.message.reply_text("⛔ این لینک، یوتیوب نیست!")

# 🧠 تنظیمات و اجرای بات
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.Document.ALL, handle_file))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_youtube))

app.run_polling()
