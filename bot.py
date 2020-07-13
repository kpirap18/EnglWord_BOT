import telebot
import config
import config_init
import logging

import datetime
import mongoengine
from random import randint, seed
from mongo_models import User_stud, Question

from aiohttp import web

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(config_init.TOKEN)
mongoengine.connect('test')

app = web.Application()

def generate_r2d2():
    #seed(datetime.now())
    return f"R{randint(0, 100)}-D{randint(0, 100)}"

def message_send_readiness():
    for stud in User_stud.objects():

@bot.message_handler(commands=["help"])
def help_messages(message):
    keyboard = telebot.types.InlineKeyboardMarkup()

    button1 = telebot.types.InlineKeyboardButton(
        config.HELP_BUTTON,
        url='telegram.me/k_ira_18')
    button2 = telebot.types.InlineKeyboardButton(
        config.HELP_BUTTON,
        url='telegram.me/alena_zayts')
    keyboard.add(button1)
    keyboard.add(button2)

    bot.send_message(message.chat.id,
                     config.HELP_MESSAGE,
                     reply_markup= keyboard)



@bot.message_handler(commands=["developers"])
def developers_messages(message):
    bot.send_message(message.chat.id, config.DEV_MESSAGE)

@bot.message_handler(commands=["start"])
def start_registration(message):
    bot.send_message(message.chat.id, "Привет! Мы с тобой наччинаем"
                                      " изучать слова, мой друг!")

    if not User_stud.objects(user_id=message.chat.id):
        queue_questions = list()

        queue_questions = [{"question_day": i, "days_left": 0}
                           for i in range(datetime.today() + config.PORTION_QUE)]
        login = message.chat.username

        if message.chat.username is None:
            login = f"[{generate_r2d2()}](tg://user&id={str(message.chat.id)})"
        stud = User_stud(
            user_id=message.chat.id,
            login=login,
            queue=queue_questions
        )
        stud.save()

        bot.send_message(message.chat.id, "Привет! Мы с тобой начинаем"
                                          "изучать слова, мой друг!")
    else:
        bot.send_message(message.chat.id, "Ты уже есть у меня в памяти!")

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)
    print(message.chat.id, message.chat.username)
    print(f"[{generate_r2d2()}](tg://user&id={str(message.chat.id)})")


if __name__ == '__main__':
    bot.polling(none_stop=True)
