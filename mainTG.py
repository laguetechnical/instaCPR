import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from core.models import ReportData
from core.queue import QueueManager
import os

queue_manager = QueueManager()
BOT_LOOP = None
BOT_TOKEN = os.getenv("BOT_TOKEN")

class TelegramProgress:
    def __init__(self, message):
        self.message = message
        self.last_text = ""

    async def update(self, text: str):
        if text == self.last_text:
            return
        self.last_text = text
        try:
            await self.message.edit_text(f"🔄 **Live Progress**\n\n{text}")
        except:
            pass

async def on_startup(application):
    global BOT_LOOP
    BOT_LOOP = asyncio.get_running_loop()

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global BOT_LOOP

    if len(context.args) < 4:
        await update.message.reply_text("Usage: /report <platform> <fullname> <copied_url> <target_url>")
        return

    platform = context.args[0].lower()
    fullname = " ".join(context.args[1:-2])
    copied_url = context.args[-2]
    target_url = context.args[-1]

    report_data = ReportData(
        platform=platform,
        fullname=fullname,
        copied_url=copied_url,
        target_url=target_url,
    )

    status_msg = await update.message.reply_text("🚀 Starting report...")

    progress_obj = TelegramProgress(status_msg)

    def progress_callback(text: str):
        if BOT_LOOP:
            asyncio.run_coroutine_threadsafe(progress_obj.update(text), BOT_LOOP)

    def completion_callback(job, success=True, error=None):
        if BOT_LOOP:
            msg = f"🎉 Report #{job.id} completed!" if success else f"❌ Report #{job.id} failed: {error}"
            asyncio.run_coroutine_threadsafe(status_msg.edit_text(msg), BOT_LOOP)

    job = queue_manager.submit(
        report_data=report_data,
        chat_id=update.effective_chat.id,
        progress_callback=progress_callback,
        completion_callback=completion_callback
    )

    await status_msg.edit_text(f"📋 Report #{job.id} queued successfully!")

def main():
    global BOT_LOOP

    queue_manager.start_worker()

    app = Application.builder().token(BOT_TOKEN).build()
    app.post_init = on_startup

    app.add_handler(CommandHandler("start", lambda u,c: u.message.reply_text("Bot is ready! Use /report")))
    app.add_handler(CommandHandler("report", report))

    print("🤖 Telegram Bot + Queue Started (Clean Architecture)")
    app.run_polling()

if __name__ == "__main__":
    main()