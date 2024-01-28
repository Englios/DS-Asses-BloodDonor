from telegram import Update
from telegram.ext import ContextTypes
from main_utils.vars import BOT_USERNAME
from .daily import schedule_daily_job

## Commands
# Init Commands
async def help_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    message = """
    Hello,I am here to serve!!!
    I am able to process these commands at the moment
    
    /help - Displays the list of commands
    
    /start - Starts me up
    /daily - Shows the latest up to date statistics 
    
    /schedule - Manually Schedules Bot Daily Job
    /schedule_stop - Stops the Daily Job
    
    /show_malaysia - Shows the trend of Malaysia Blood Donation
    /show_states - Shows the trend of Malaysian States Blood Donation
    /show_retention - Shows the retention trend of Malaysia Blood Donation
    
    /questions - Displays the list of questions you can as me!
    /info - Shows further info of the Blood Donation Bot
    
    New commands will be added in the future!!!
    """
    await update.message.reply_text(message)

async def start_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    message = f"""
    Hello! Thank you for chatting with me. I am here to serve you!\n\nMy current capabilities are limited, but you can tag me {BOT_USERNAME} and ask me the following questions:\n\n- How are blood donations in Malaysia or specific states trending?\n- How well is Malaysia retaining blood donors?\n\nTo see all the list of questions you can ask please type in /questions \n\nI will also provide daily statistics of blood donation trends within Malaysia, including a comparison of data from three days ago.\n\nFeel free to ask me anything related to blood donations in Malaysia. I'm here to help!
    """
    schedule_daily_job(update,context)
    await update.message.reply_text(message)

## Others
async def info_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    message=f'''
    This Bot was made by Muhammad Alif Aiman.\nThe bot takes data from KKM and provides trends and statistics of Blood Donation within Malaysia.\n\nAll data can be acquired and seen from KKM's website (https://github.com/MoH-Malaysia/data-darah-public).\n\nTo see the implementation of the bot, please visit the GitHub repository at: https://github.com/Englios/DS-Asses-BloodDonor.
    '''
    await update.message.reply_text(message)
    
async def questions_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    message=f'''
    To ask me questions please tag me first {BOT_USERNAME}!!\nI am not too intelligent at my current iteration,So please ask the questions with the some keywords below :\n\n- How are **blood donations** in **malaysia** **trending**?\n- How are **blood donations** in the **states** **trending**?\n- How well is **Malaysia** **retaining** **blood donors**?\n-What is the trend of **New Donors** in **Malaysia**?\n\n More questions will be added down the line!!!
    '''
    await update.message.reply_text(message)

#Stop Bot
async def stop_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    
    await context.bot.send_message(chat_id=chat_id,text='Shutting Down...\nTill we meet again :)')
    await context.bot.stop_polling()
