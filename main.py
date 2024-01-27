import logging

from bot import commands,daily,responses,show_commands
from main_utils import vars
from telegram.ext import Application, CommandHandler, MessageHandler,Updater,filters

def main():
    
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger()
    
    print('Starting Bot')
    app = Application.builder().token(vars.TELEGRAM_BOT_KEY).build()
    
    #Commands
    app.add_handler(CommandHandler('help',commands.help_command))
    app.add_handler(CommandHandler('start',commands.start_command))
    app.add_handler(CommandHandler("info", commands.info_command))
    app.add_handler(CommandHandler("questions", commands.questions_command))
    
    # Daily Commands
    app.add_handler(CommandHandler('daily',daily.send_daily))
    app.add_handler(CommandHandler("schedule", daily.schedule_daily_job))
    app.add_handler(CommandHandler("schedule_stop", daily.stop_daily_job))
    
    # Show Commands
    app.add_handler(CommandHandler('show_malaysia',show_commands.show_malaysia_command))
    app.add_handler(CommandHandler('show_states',show_commands.show_states_command))
    app.add_handler(CommandHandler('show_retention',show_commands.show_retention_command))
    
    
    #Messages
    app.add_handler(MessageHandler(filters.TEXT,responses.handle_message))
    #Errors
    app.add_error_handler(responses.error)


    #Polling
    print("Polling....")
    
    try:
        app.run_polling(poll_interval=3)
    except KeyboardInterrupt:
        print("Stopping bot...")
        commands.stop_bot(app)
        print("All tasks cancelled.")
    

if __name__ == '__main__':
    main()