import telebot
import requests
import json
import lxml.html
from lxml import etree

from config import *
from extensions import *

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start","help"])
def start_help(message: telebot.types.Message):
    text = "Привет\nВводи валюты через пробел\nСначала валюту цену которой ты хочешь узнать,\nзатем валюту в которой ты хочешь узнать, а затем количество\n"\
           "Например: RUB USD 4\n"\
            "Доступные команды:\n /values,/start,/help"

    bot.send_message(message.chat.id,text)
@bot.message_handler(commands=["values"])
def val(message: telebot.types.Message):
    text = "Доступные валюты\nUSD\nRUB\nEUR\nИли любая другая валюта если ты знаешь её кодировку"
    bot.send_message(message.chat.id,text)
@bot.message_handler(content_types=["text"])
def val(message: telebot.types.Message):
    values = message.text.split(" ")
    values = list(map(str.upper,values))
    try:
        result = Counter.get_price(values)
    except API_Exceptions as e:
        bot.reply_to(message, e)

    except Exception as e:
        bot.reply_to(message, e)
    else:
        text = f"Цена {values[2]} {values[0]} в {values[1]} равна {result}"
        bot.send_message(message.chat.id, text)
bot.polling(non_stop = True)