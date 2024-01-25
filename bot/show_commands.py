from telegram import Update
from telegram.ext import ContextTypes
from main_utils.vars import BOT_USERNAME

## Show Commands  
async def show_malaysia_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('What would you like to see?')
    
async def show_states_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('What would you like to see?')
    
async def show_retention_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('What would you like to see?')