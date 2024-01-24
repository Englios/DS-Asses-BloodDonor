import asyncio
import logging,pytz

from telegram import Update
from telegram.ext import ContextTypes
import os

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

#Daily Messaging
tasks = []
async def daily_msg(context, chat_id):
    while True:
        photo_path = os.path.join(os.getcwd(), "images", "test1.png")
        await context.bot.send_photo(chat_id=chat_id, photo=open(photo_path, 'rb'))
        await asyncio.sleep(30)  # Wait for 30 seconds

async def send_daily(update: Update, context: ContextTypes.DEFAULT_TYPE,_tasks:list = tasks):
    chat_id = update.message.chat_id
    task = asyncio.create_task(daily_msg(context, chat_id))
    _tasks.append(task)
    await update.message.reply_text('Daily Statistics')
    
async def stop_bot(update: Update, context: ContextTypes.DEFAULT_TYPE,_tasks:list = tasks):
    for task in _tasks:
        task.cancel()
    await context.bot.stop_polling()