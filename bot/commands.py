from telegram import Update
from telegram.ext import ContextTypes, CallbackContext
from utils.vars import BOT_USERNAME
from .daily import schedule_daily_job

# Commands
async def start_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    message = f"""
    Hello! Thank you for chatting with me. I am here to serve you!\n\nMy current capabilities are limited, but you can tag me {BOT_USERNAME} and ask me the following questions:\n\n- How are blood donations in Malaysia or specific states trending?\n- How well is Malaysia retaining blood donors?\n\nI will also provide daily statistics of blood donation trends within Malaysia, including a comparison of data from three days ago.\n\nFeel free to ask me anything related to blood donations in Malaysia. I'm here to help!
    """
    schedule_daily_job(update,context)
    await update.message.reply_text(message)
    
async def help_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    message = """
    Hello,I am here to serve!!!
    I am able to process these commands at the moment
    
    /start - Starts me up
    /daily - Shows the latest up to date statistics 
    /help - Displays the list of commands
    /schedule - Manually Schedules Bot Daily Job
    /schedule_stop - Stops the Daily Job
    /show - Shows the trend of Malaysia Blood Donation
    
    New commands will be developed in the future
    """
    await update.message.reply_text(message)
    
async def custom_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    message = """
    Hello,Thanks for Chatting with me! I am here to serve!!!
    """
    await update.message.reply_text('This is a custom command')
    
async def show_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('What would you like to see?')
    
async def info_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    message=f'''
    This Bot was made by Alif Aiman.
    All data can be acquired and seen from KKM's website (https://github.com/MoH-Malaysia/data-darah-public)
    To see implementation of the bot please see 
    '''
    await update.message.reply_text('What would you like to see?')