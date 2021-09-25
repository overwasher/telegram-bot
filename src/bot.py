import telegram
from telegram.ext import *
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor
import handlers
import inspect
import peewee
import json
import click
import sys

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

loop = asyncio.get_event_loop()

#Load configuration with secrets
config = {}
with open("/run/secrets/config.json", "r") as f:
    config = json.load(f)

bot_token = config["bot-token"]

#Make sure to print an error if bot token is empty
if bot_token == "":
    print(click.style("Bot token is empty, make sure that you have set it in ./secrets/config.json",fg="red"))
    sys.exit()

updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher


start_handler = CommandHandler('start', handlers.start_handler)
dispatcher.add_handler(start_handler)

machinestatus_handler = MessageHandler(Filters.text & ~Filters.command, handlers.machinestatus_handler)
dispatcher.add_handler(machinestatus_handler)


thread_pool_executor = ThreadPoolExecutor()

loop.run_in_executor(thread_pool_executor,updater.start_polling)
loop.run_forever()






 
