import asyncio
import pytz
import logging, datetime, pytz
from utils.vars import BOT_USERNAME

from telegram import Update
from telegram.ext import ContextTypes,CallbackContext
from datetime import time,datetime
import os

# Commands
async def start_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    message = f"""
    Hello,Thanks for Chatting with me! I am here to serve!!!
    My current capabilites are limited,but you may tag me {BOT_USERNAME} and aske me these questions
    -   How are blood donations in Malaysia / states trending ?
    -   How well is Malaysia retaining blood donors?
    """
    await update.message.reply_text(message)
    
async def help_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    message = """
    Hello,I am here to serve!!!
    I am able to process these commands at the moment
    
    /start - Starts me up
    /daily - Activate my daily function 
    /help - Displays the list of commands
    /custom - Nothing At the moment
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