import os

def get_message_string(file_path):
    with open(file_path,'r',encoding='utf-8') as f:
        message = f.read()
    return message


def daily(context, chat_id):
    photo_path = os.path.join(os.getcwd(), "images", "test1.png")
    daily_message = os.path.join(os.getcwd(),"daily_texts","daily_message.txt")
    context.bot.send_message(chat_id=chat_id, text=get_message_string(daily_message))