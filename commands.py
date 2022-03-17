
from telebot import types
import os
import telebot
API_KEY= '5101529403:AAHtdX8KBLI_In7rg5SCIEEvAH34m7Ut8MI'
bot = telebot.TeleBot(API_KEY)
from TextDict import *
# this is the start message, it's sending first message (starting message) That show how to use the bot and its commamd
@bot.message_handler(commands=["تحوت","start"])
def start(message):
    bot.send_message(message.chat.id,text =Text['StartMessage'])

# Lecture Schedule png photo
@bot.message_handler(commands=["الجدول",'schedule'])
def schedule(message):
    photo = open('Subjects/schedule.png', 'rb')
    bot.send_photo(message.chat.id, photo)

# Roadmap command
@bot.message_handler(commands=["خريطة_التعلم",'roadmap'])
def Roadmap(message):
    bot.send_message(message.chat.id,text = Text['RoadmapMessage'])

#collaborators command, it's opening a text file `collaborators.txt` and send its content
@bot.message_handler(commands=["المساهمين",'collaborators'])
def collaborators(message):
    with open('collaborators.txt','rb') as f:
        data = f.read()
        bot.send_message(chat_id=message.chat.id,text=data)
# Source code command
@bot.message_handler(commands=["الكود",'source_code'])
def source_code(message):
    bot.send_message(chat_id=message.chat.id,text=Text['sourceCodeMessage'])

    #help message command
@bot.message_handler(commands=["مساعدة",'help'])
def HowToUse(message):
    bot.send_message(chat_id=message.chat.id,text=Text['HelpMessage'])


