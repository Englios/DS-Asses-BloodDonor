import logging
import os

from telegram import Update
from telegram.ext import ContextTypes

from datetime import time
from .utils.helper import get_message_string
from .utils import helper as h

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Daily Messaging
async def daily_msg(context, chat_id):
    photo_path = os.path.join(os.getcwd(), "images", "test1.png")
    daily_message = os.path.join(os.getcwd(),"daily_texts","daily_message.txt")
    # await context.bot.send_photo(chat_id=chat_id, photo=open(photo_path, 'rb'))
    await context.bot.send_message(chat_id=chat_id, text=get_message_string(daily_message))

async def send_daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    await daily_msg(context, chat_id)
    # await update.message.reply_text('Daily Statistics')
    
async def stop_daily_job(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.job_queue.stop()

def schedule_daily_job(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    context.job_queue.run_daily(lambda context: daily_msg(context, chat_id), interval=20)

