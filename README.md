# Telegram Blood Donation Bot

## Introduction
This is a Telegram bot that makes visualization according to MoH Blood Donations Data. It is written in Python and uses the [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) library.

## Usage
The bot is currently hosted on Digital Ocean via the Docker Container. You can find it [here](https://t.me/blooddonationbot).Alternatively, you can host it yourself by following the instructions below.

## Features
- Daily Job that sends the latest up to date statistics
- Trend of Malaysia Blood Donation
- Trend of Malaysian States Blood Donation
- Retention trend of Malaysia Blood Donation
- Bot is able to answer questions regarding Blood Donation in Malaysia

### Installation
1. Clone this repository.
2. Install the required packages using `pip install -r requirements.txt`.
3. Create a new bot using [BotFather](https://t.me/botfather) and get the API token.
4. Run `python3 main.py` and enter the API token when prompted.
5. The bot should be up and running now.

#### Alternative Installation
1. Create a new bot using [BotFather](https://t.me/botfather) and get the API token.
2. Use docker-compose to build the image and run the container.
3. Run `docker exec -it <container_name> python3 main.py` and enter the API token when prompted.
4. The bot should be up and running now.

### Commands
- `/help` - Displays the list of commands
- `/start` - Starts me up
- `/daily` - Shows the latest up to date statistics 
- `/schedule` - Manually Schedules Bot Daily Job
- `/schedule_stop` - Stops the Daily Job
- `/show_malaysia` - Shows the trend of Malaysia Blood Donation
- `/show_states` - Shows the trend of Malaysian States Blood Donation
- `/show_retention` - Shows the retention trend of Malaysia Blood Donation
- `/show_new_donors` - Shows the trend of new donors in Malaysia
- `/questions` - Displays the list of questions you can ask me!
- `/info` - Shows further info of the Blood Donation Bot
