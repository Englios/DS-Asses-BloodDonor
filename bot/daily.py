import os

from telegram import Update
from telegram.ext import ContextTypes

from datetime import time
from .utils.helper import get_message_string
from .utils import helper as h
from .show_commands import show_all



# Daily Messaging

async def daily_msg(update:Update,  context:ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    daily_message = os.path.join(os.getcwd(),"daily_texts","daily_message.txt")
    await context.bot.send_message(chat_id=chat_id, text=get_message_string(daily_message))
    
async def daily_viz(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await show_all(update,context)

async def send_daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    await update.message.reply_text('Daily Statistics')
    await daily_msg(context, chat_id)
    await update.message.reply_text('Daily Charts')
    await daily_viz(update,context)
    
async def send_daily_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    await update.message.reply_text('Daily Statistics')
    await daily_msg(context, chat_id)
    
async def send_daily_viz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    await update.message.reply_text('Daily Charts')
    await daily_viz(update,context)

async def stop_daily_job(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.job_queue.start()
    
async def stop_daily_job(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.job_queue.stop()

#? Depreceated
async def schedule_daily_job(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    
    daily_msg_wrap = lambda x=context:daily_msg(update, x)
    daily_viz_wrap = lambda x=context:daily_viz(update, x)
    
    # Schedule daily messages at 9 AM and 2 PM
    context.job_queue.run_daily(daily_msg_wrap, time=time(hour=9))
    context.job_queue.run_daily(daily_msg_wrap, time=time(hour=14))

    # Schedule daily visualization at 9 AM and 2 PM
    context.job_queue.run_daily(daily_viz_wrap, time=time(hour=9))
    context.job_queue.run_daily(daily_viz_wrap, time=time(hour=14))

