from telegram import Update
from telegram.ext import ContextTypes
from main_utils.vars import BOT_USERNAME

## Show Commands  
async def show_malaysia_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    message = f"""
    Hello here is the latest statistics for Malaysia
    """
    await context.bot.send_photo(chat_id=chat_id,
                                 photo=open('./images/trend_donations_malaysia.jpg', 'rb'),
                                 caption = f'As we can see,Malaysia is on the rise with Blood Donations,which means more and more people are donating blood.\nThe data for 2024 is still in collection,but it will most likely rise from previous years')
    
    await context.bot.send_photo(chat_id=chat_id,
                                 photo=open('./images/trend_7_day_avg_malaysia_2023.jpg', 'rb'),
                                 caption = f'By Taking a closer look over 2023 - 2024.\nIt can be seen that our daily Blood Donations are stable,with daily an average daily donation count.\nThe valley formed around 2023-4 to 2023-5 is most likely due to fasting month,where less blood donations are peformed by the Muslim population.')
    
    await context.bot.send_photo(chat_id=chat_id,
                                photo=open('./images/trend_7_day_avg_malaysia_2021.jpg', 'rb'),
                                caption = f'This is further reinforced by looking at the data from 2021 - 2022,where a valley is formed early in 2021-5,which for that year,Ramadhan falls on May.')
    
    await context.bot.send_photo(chat_id=chat_id,
                                 photo=open("./images/"))

async def show_states_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    
    await context.bot.send_message(chat_id=chat_id,text='Here are the trends in Malaysian States.')
    
    await context.bot.send_photo(chat_id=chat_id,
                                 photo=open('/images/donation_trend_all_years.jpg', 'rb'),
                                 caption = f'')
    
    await context.bot.send_photo(chat_id=chat_id,
                                 photo=open('./images/trend_7_day_avg_malaysia_2023.jpg', 'rb'),
                                 caption = f'By Taking a closer look over 2023 - 2024.\nIt can be seen that our daily Blood Donations are stable,with daily an average daily donation count.\nThe valley formed around 2023-4 to 2023-5 is most likely due to fasting month,where less blood donations are peformed by the Muslim population.')
    
    await context.bot.send_photo(chat_id=chat_id,
                                photo=open('./images/trend_7_day_avg_malaysia_2021.jpg', 'rb'),
                                caption = f'This is further reinforced by looking at the data from 2021 - 2022,where a valley is formed early in 2021-5,which for that year,Ramadhan falls on May.')
    
    await context.bot.send_photo(chat_id=chat_id,
                                 photo=open("./images/"))
    
    await context.bot.send_message(chat_id=chat_id,text='Here are the trends in Malaysian States.')
    
async def show_retention_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('What would you like to see?')