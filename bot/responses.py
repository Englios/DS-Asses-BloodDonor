import asyncio
import logging
from main_utils import vars

from telegram import Update
from telegram.ext import ContextTypes

BOT_USERNAME = vars.BOT_USERNAME

# Responses
def handle_response(text:str) -> str:
    processed:str = text.lower()
    
    match processed:
        case 'how are blood donations in malaysia trending':
            return 'hi'
        
        case 'how are blood donations in the states trending':
            return None
        
        case 'how well is Malaysia retaining blood donors':
            return None
        
        case _:
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
    