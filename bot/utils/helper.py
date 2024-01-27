import os
import nltk

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def get_message_string(file_path):
    with open(file_path,'r',encoding='utf-8') as f:
        message = f.read()
    return message


def daily(context, chat_id):
    photo_path = os.path.join(os.getcwd(), "images", "test1.png")
    daily_message = os.path.join(os.getcwd(),"daily_texts","daily_message.txt")
    context.bot.send_message(chat_id=chat_id, text=get_message_string(daily_message))
    
def tokenize_words(sentence:str):
    return word_tokenize(sentence)
    
def get_lemmatized_words(sentence:str):
    tokens = word_tokenize(sentence)
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in tokens if word.casefold() not in stop_words]
    
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word,pos='v') for word in filtered_words]    
    return lemmatized_words 