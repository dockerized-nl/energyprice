import pytz
from aiogram import Bot, Dispatcher, executor, types
import rich
import telebot
import os
from datetime import timedelta
from datetime import datetime
import matplotlib.pyplot as plt
import requests


def handle_response():
    current_date = datetime.now(pytz.timezone('Europe/Amsterdam'))
    yesterday = current_date + timedelta(days=-1)


    URL = f"https://api.energyzero.nl/v1/energyprices?fromDate={yesterday.strftime('%Y-%m-%d')}T22:00:00.000Z&tillDate={current_date.strftime('%Y-%m-%d')}T22:00:00.000Z&interval=4&usageType=1&inclBtw=true"
    page = requests.get(URL)

    output_page = page.json()

    output = ""

    average = output_page['average']


    for item in output_page['Prices']:
        hour = int(item['readingDate'].split('T')[-1].replace('Z', '')[:2])
        hour += 2
        if hour == 24:
            hour = 00
        elif hour == 25:
            hour = 1
        output += f"Tijd: {hour} Prijs: {item['price']}"
        output += "\n"

    labels = []
    values = []

    for item in output_page['Prices']:
        labels.append(item['readingDate'].split('T')[-1].replace('Z', '')[:2])
        values.append(item['price'])
        
    return output


BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def welcome(message: types.Message):
    bot.reply_to(
        message, "Hello! Im Energy price Bot, Please use /prijs to get the charts")


@bot.message_handler(commands=['Gino', 'Jesse'])
def welcome(message: types.Message):
    bot.reply_to(message, "Gino & Jesse! Please help the bot is down!")

# @bot.message_handler(func=lambda msg: True)
# def echo_all(message):
#    bot.reply_to(message, message.text)


@bot.message_handler(commands=['prijs'])
def logo(message: types.Message):
    current_date = datetime.now(pytz.timezone('Europe/Amsterdam'))
    output = handle_response()
    bot.send_photo(message.chat.id, open(
        f"images/price_plot_{current_date.strftime('%Y-%m-%d')}.png", "rb"))
    bot.reply_to(message, f"{output}")


bot.infinity_polling()
