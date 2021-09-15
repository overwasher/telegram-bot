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
import requests
import time
import click
from datetime import datetime
import timeago

#************************************
#     Global variables module
#************************************
loop = asyncio.get_event_loop()

db = SqliteDatabase('../data/overwasher.db')


num = 3
config = {}
with open("/run/secrets/config.json", "r") as f:
    config = json.load(f)

bot_token = config["bot-token"]

if bot_token == "":
    print(click.style("Bot token is empty, make sure that you have set it in ./secrets/config.json",fg="red"))
    sys.exit()
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

def notify_admins(message):
    chat_id_vy=314645303
    #chat_id_dc=379529027
    send_message(chat_id=chat_id_vy, text = "SOMETHING BROKE. AGAIN. FIX THIS SHIT")
    #send_message(chat_id=chat_id_dc, text = "DID YOU BREAK API AGAIN? STOP IT!")

#************************************
#        Exceptions module
#************************************

class BadResponse(Exception):
    pass

#....................................
#     Helpers submodule                                  
#....................................

def safe_list_get (l, idx, default):
  try:
    return l[idx]
  except (IndexError, ValueError):
    return default

def get_data_from_backend():
    while True:
        try:
            response = requests.get('https://overwatcher.ow.dcnick3.me/status/v1', timeout=5)
            # If the response was successful, no Exception will be raised
            response.raise_for_status()
            if not response.status_code == 200:
                raise BadResponse(response.status_code)
        except HTTPError as http_err:
            logging.exception(http_err)
            time.sleep(2)
            continue
        except requests.exceptions.RequestException as err:
            logging.exception(err)
            raise err
        except BadResponse as err:
            logging.exception(err)
            raise err
        print(click.style(response.json(), fg="yellow"))
        return response.json()


    
def form_message():
    resp = get_data_from_backend()
    message = f"All known machines:\n\n"
    machines = ""

    try:
        for sensor_node in resp:
            print(click.style(sensor_node, fg="red"))

            t =datetime.utcfromtimestamp(sensor_node["lastContact"]//1000).strftime('%Y-%m-%d %H:%M:%S')
            state = sensor_node["state"]
            state = state.replace("inactive", "free")
            state = state.replace("active", "busy")

            try:
                location = sensor_node["id"]
                type_ = ""
                if "wash" in location:
                    type_ = "Washer"
                elif "dry" in location:
                    type_ = "Dryer"
                else:
                    raise ValueError("Uknown type enountered")
                location = re.findall(r'\d+', location)
                print(click.style(location, fg="red"))
                location = f"Dorm {location[0]}, Floor {location[1]}, {type_} {location[2]}"
            except (IndexError, ValueError, Exception) as err:
                logging.exception(err)
                continue

            emoji_state = ""
            if state == "unknown":
                emoji_state = "❔" #white question mark
            elif state == "busy":
                emoji_state = "🛑"
            elif state == "free":
                emoji_state = "🟢"
            else:
                emoji_state = ""

            machines += f"{location} is {state}{emoji_state}\nLast updated: {timeago.format(t, datetime.utcnow())}\n\n"
    except (IndexError, ValueError, Exception) as err:
        message = "Sorry, we are having Backend Issues today\nAdmins will be notified and probably will fix it.."
        machines = ""
        logging.exception(err)
        notify_admins(err)

    print(click.style(machines, fg="red"))
    if machines == "":
        message = "We do not know anything about machines now.."
    else:
        message+=machines

    return message

#************************************
#         User module
#************************************


def start_handler(update, context):
    alias = update.effective_user.username #get persons username from telegram
    chat_id=update.message.chat_id

    keyboard = telegram.ReplyKeyboardMarkup([["📊Status", "❌Cancel"]])

    send_message(chat_id=chat_id, text="Hello!\n I am overwasher bot \n I will help you get status of washing and drying mashines")
    send_message(chat_id=chat_id, text="P.S. Currently only a few washing mashines are supported!", reply_markup = keyboard)


def machinestatus_handler(update, context):
    alias = update.effective_user.username #get persons username from telegram
    chat_id=update.message.chat_id
    print(f"\n\n\n\n\n{update.message}\n\n\n")
    text = update.message.text.lower()
    if (text == "📊status") or (text == "status"):
        message = form_message()
        send_message(chat_id=chat_id, text = message)
    elif (text == "❌cancel") or (text == "cancel"):
        keyboard = telegram.ReplyKeyboardRemove()
        send_message(chat_id=chat_id, text="Alrighty. Be sure to say /start when you want to chat next time", reply_markup = keyboard)
    else:
        update.message.reply_text("What is das?")





















