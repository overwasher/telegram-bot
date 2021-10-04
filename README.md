##### [Home repo](https://github.com/overwasher/home/) | [Overwatcher code](https://github.com/overwasher/overwatcher) | [Sensor Node code](https://github.com/overwasher/esp-firmware) | [Telegram bot code](https://github.com/overwasher/telegram-bot) | [Task Tracker](https://taiga.dcnick3.me/project/overwasher/)

# Overwasher: telegram-bot

## Description

This component of Overwasher project provides a user-facing interface.

Currently it is very simple and just wraps data in fancy text and emojis.


### Demo

![Demo dialog](https://github.com/overwasher/telegram-bot/blob/main/Demo.png)

Currently we host an instance of this bot at [@overwasher_bot](https://t.me/overwasher_bot)

*Note: This bot gathers data from Innopolis dorms and is under development so it may be unavailable at some points in time*

### Development stack

Bot is written using python3 and [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) framework. 

*Note: little to no OOP approaches are used in this component as it is common for telegram bots*

## Setup

*Disclaimer: project is in its early stages. Much may change relatively soon. Stability is not guaranteed.*

If you are planning to host this bot yourself, you are better off using docker as updates and machine restarts will not affect bot installed this way too much.

For development purposes an undockerised setup is faster.

### Dockerised
1. Clone repo `git clone https://github.com/overwasher/telegram-bot.git`
2. Launch `cd telegram-bot` 
3. Obtain bot token from [BotFather](https://core.telegram.org/bots#6-botfather) in telegram
4. Write your token into `./secrets/config.json`
5. Launch `sudo docker-compose up --build -d`

*Note*: if you run on docker on debian you may need to change version in `docker-compose.yml` to supported one like 3.3

### Undockerised
1. Clone repo `git clone https://github.com/overwasher/telegram-bot.git`
2. Launch `cd telegram-bot` 
3. Obtain bot token from [BotFather](https://core.telegram.org/bots#6-botfather) in telegram
4. Write your token into `./secrets/config.json`
5. Install all dependencies via `pip3 install -r requirements.txt`
6. Run `python3 ./src/bot.py`

## How to contribute

Currently, the project is in heavy development and may change a lot in the nearest future. 

*We do not recommend contributing at this stage*. 

Later, when project becomes more stable, we may create some contribution guidelines for everyone to use. 
