import asyncio
import logging
from .show_commands import *

from main_utils import vars
from .utils import helper
from telegram import Update
from telegram.ext import ContextTypes


BOT_USERNAME = vars.BOT_USERNAME

# Responses
def handle_response(text:str,update,context) -> str:
    processed_text = helper.get_lemmatized_words(text.lower())

    if all(keyword in processed_text for keyword in ['malaysia','trend','blood','donations']):
        return show_malaysia_command()
        
    elif all(keyword in processed_text for keyword in ['states','trend','blood','donations']):
        return show_states_command()
        
    elif any(keyword in processed_text for keyword in ['retain', 'return', 'regular','lapse']):
        return show_retention_command()
    
    elif any(keyword in processed_text for keyword in ['new','blood','donations','donor']):
        return show_new_donors_command()
    
    else:
        return 'I am not programmed to understand that yet'

async def handle_message(update:Update,context:ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text:str = update.message.text  
    
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(vars.BOT_USERNAME, '').strip()
            response:str = handle_response(new_text)
            
        else:
            return 
    else:
        response:str = handle_response(text)
        
    print('Bot:',response)
    await update.message.reply_text(response)
    
def error(update:Update,context:ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')
    