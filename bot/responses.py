from .show_commands import *

from main_utils import vars
from .utils import helper
from telegram import Update
from telegram.ext import ContextTypes

BOT_USERNAME = vars.BOT_USERNAME

# Responses
def handle_response(text:str) -> str:
    processed_text = helper.get_lemmatized_words(text.lower())

    if all(keyword in processed_text for keyword in ['malaysia','states','trend','blood','donations']):
        return "Here's the trend in the States"
    
    elif all(keyword in processed_text for keyword in ['malaysia','trend','blood','donations']):
        return "Here's the trend in Malaysia"
        
    elif any(keyword in processed_text for keyword in ['retain', 'return', 'regular','lapse']):
        return "Here's how many donors are returning!"
    
    elif any(keyword in processed_text for keyword in ['new','blood','donations','donor']):
        return "Here's the trend of New Blood Donors"
    
    else:
        return 'I am not programmed to understand that yet or you '

#Show parser
async def show_parser(response:str,update,context):
    if response == "Here's the trend in Malaysia":
        await show_malaysia_command(update, context)
        
    elif response == "Here's the trend in the States":
        await show_states_command(update, context)
        
    elif response == "Here's how many donors are returning!":
        await show_retention_command(update, context)
    
    elif response == "Here's the trend of New Blood Donors":
        await show_new_donors_command(update, context)
    
    else:
        pass

#Handle Message Function
async def handle_message(update:Update,context:ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text:str = update.message.text  
    
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    if message_type in ['group','supergroup']:
        if BOT_USERNAME in text:
            new_text: str = text.replace(vars.BOT_USERNAME, '').strip()
            response:str = handle_response(new_text)
        else:
            return 
    else:
        response:str = handle_response(text)
        
    print('Bot:',response)
    await update.message.reply_text(response)
    await show_parser(response,update,context)

#Handle Errors
def error(update:Update,context:ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')
    