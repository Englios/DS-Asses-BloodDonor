import bot.bot as bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters
def main():
    
    print('Starting Bot')
    app = Application.builder().token(bot.TOKEN).build()
    
    #Commands
    app.add_handler(CommandHandler('start',bot.start_command))
    app.add_handler(CommandHandler('help',bot.help_command))
    app.add_handler(CommandHandler('custom',bot.custom_command))
    app.add_handler(CommandHandler('daily',bot.send_daily))
    
    #Messages
    app.add_handler(MessageHandler(filters.TEXT,bot.handle_message))
    #Errors
    app.add_error_handler(bot.error)
    
    #Polling
    print("Polling....")
    
    try:
        app.run_polling(poll_interval=3)
    except KeyboardInterrupt:
        print("Stopping bot...")
        bot.stop_bot()
        print("All tasks cancelled.")
    

if __name__ == '__main__':
    main()