import telegram
from telegram.ext import *
import logging
import asyncio
import re
import os
from copy import deepcopy
import json
import time
import tempfile
from pprint import pprint
from peewee import *


#************************************
#     Global variables module
#************************************
loop = asyncio.get_event_loop()

db = SqliteDatabase('eurobot.db')


num = 3
bot_token = ""
bot = telegram.Bot(token=bot_token)


kb = [[telegram.KeyboardButton('ВСЁ!')]]

kb_markup = telegram.ReplyKeyboardMarkup(kb)

attachment_id = 0



#************************************
#    Telegram wrappers module
#************************************


TIMEOUT = 80 #Timeout and retries for sending telegram messages
RETRIES = 10


def __send_something(send_function, **kwargs): #helper function that wraps all telegram messages to retry in case of timeout
    global TIMEOUT
    global RETRIES
    i = 0 
    while (True):
        try:
            time.sleep(2**i)
            if (i>RETRIES):
                break
            send_function(**kwargs, timeout = TIMEOUT, parse_mode="HTML")
            i+=1
            break
        except telegram.error.TimedOut:
            logging.warning("Sending telegram message timed out\n")
            continue
        except telegram.error.NetworkError as e:
            logging.warning(e)
            logging.exception("Some network error happened with Telegram")
            continue
        except ConnectionResetError as e:
            logging.warning(e)
            logging.exception("Some network error happened with Telegram")
            continue

def send_media_group(**kwargs):
    global bot
    __send_something(bot.send_media_group, **kwargs)

def send_photo(**kwargs):
    global bot
    __send_something(bot.send_photo, **kwargs)
         
def send_audio(**kwargs):
    global bot
    __send_something(bot.send_audio, **kwargs)

def send_message(**kwargs):
    global bot
    __send_something(bot.send_message, **kwargs)
            
def send_document(**kwargs):
    global bot
    __send_something(bot.send_document, **kwargs)
        

#************************************
#          Regexp module
#************************************

def matches_string(regex, string):
    m = re.search(regex, string)
    if (m == None):
        return False
    return m.span()[0]==0 and m.span()[1]==len(string)



#************************************
#         ORM definitions module
#************************************

class Project(Model):
    id = IntegerField(unique = True, primary_key = True)
    name = CharField(unique = True)
    password = CharField(default = "")
    user_password = CharField(default = "") #TODO add user passwords so that not everyone can enroll
    
    class Meta:
        database = db


#************************************
#      Administrators module
#************************************




#....................................
#     Helpers submodule                                  
#....................................

def safe_list_get (l, idx, default):
  try:
    return l[idx]
  except (IndexError, ValueError):
    return default

def get_data_from_backend():
    return ""
    
def form_message():
    get_data_from_backend()
    return ""

#************************************
#         User module
#************************************


def start_handler(update, context):
    alias = update.effective_user.username #get persons username from telegram
    chat_id=update.message.chat_id

    keyboard = telegram.ReplyKeyboardMarkup([["📊Status", "Cancel"]])

    send_message(chat_id=chat_id, text="Hello!\n I am overwasher bot \n I will help you get status of washing and drying mashines")
    send_message(chat_id=chat_id, text="P.S. Currently only a few washing mashines are supported!", reply_markup = keyboard)


def machinestatus_handler(update, context):
    alias = update.effective_user.username #get persons username from telegram
    chat_id=update.message.chat_id
    print(f"\n\n\n\n\n{update.message}\n\n\n")
    if (update.message.text == "📊Status"):
        message = form_message()
        send_message(chat_id=chat_id, text = "NotYetImplementedException")
    else:
        update.message.reply_text("What is das?")





















