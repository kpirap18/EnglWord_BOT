import telebot
import json
import multiprocessing
import schedule
import config
import time
import os

import logging

import datetime
import mongoengine

from dbinstances import User_stud, Question
from random import randint, seed


logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(config.TOKEN)

mongoengine.connect(
    db=config.DB_NAME,
    username=config.DB_USER,
    password=config.DB_PASS,
    host=config.DB_HOST,
    port=27017
)

def generate_r2d2():
    seed(datetime.now())
    return f"R{randint(0, 100)}-D{randint(0, 100)}"

def message_send_readiness():
    """
        Отправка всем вопрос о готовности
    """
    for stud in User_stud.objects():
        stud = send_single_conf(stud, True)
        stud.save()

def send_single_conf(stud, is_):
    """
        Вопрос о готовности пользователя
    """
    mark_ = telebot.types.InlineKeyboardMarkup()
    mark_.add(telebot.types.InlineKeyboardButton(text = config.READY_BTN,
                                                 callback_data = config.READY_BTN ))

    if is_:
        message = "📚 Готовы ответить на пару вопросиков от меня?"

    bot.send_message(stud.user_id, message, reply_markup=mark_)

    return stud

@bot.message_handler(commands=["help"])
def help_messages(message):
    """
        Информация помощи
    """
    keyboard = telebot.types.InlineKeyboardMarkup()

    button1 = telebot.types.InlineKeyboardButton(
        config.HELP_BUTTON,
        url='telegram.me/k_ira_18')
    keyboard.add(button1)

    '''button2 = telebot.types.InlineKeyboardButton(
        config.HELP_BUTTON,
        url='telegram.me/alena_zayts')
    keyboard.add(button2)'''

    bot.send_message(message.chat.id,
                     config.HELP_MESSAGE,
                     reply_markup= keyboard)

@bot.message_handler(commands=["developers"])
def developers_messages(message):
    """
        Информация о разработчиках
    """
    bot.send_message(message.chat.id, config.DEV_MESSAGE)

@bot.message_handler(commands=["start"])
def start_registration(message):
    """
        Запись некоторых данных пользователя в бд
    """

    if not User_stud.objects(user_id=message.chat.id):
        '''login = message.chat.username

        if message.chat.username is None:
            login = f"[{generate_r2d2()}](tg://user&id={str(message.chat.id)})"'''

        msg = bot.send_message(message.chat.id,
                               "Скажи мне, пожалуйста, как тебя зовут?")
        bot.register_next_step_handler(msg, name_ask)

    else:
        bot.send_message(message.chat.id, "Ты уже есть у меня в памяти!")

def name_ask(message):
    """
        Запись имени
    """
    
    if type(message.text) == str:
        user_name = message.text
        stud = User_stud(
            user_id=message.chat.id,
            user_name = user_name,
            user_status = "stop"
        )
        stud.save()
        bot.send_message(message.chat.id, "👋 Привет, " + user_name +
                                          "! Мы с тобой начинаем"
                                          " изучать слова, мой друг!")
    else:
        mssg = bot.send_message(message.chat.id, "😔 Прости, я тебя не понимаю,"
                                                 "попробуй еще раз")
        bot.register_next_step_handler(mssg, name_ask)

def schedule__():
    schedule.every().day.at("13:00").do(message_send_readiness)

    while True:
        schedule.run_pending()
        time.sleep(1)


def parse_questions():
    pass


if __name__ == "__main__":
    multiprocessing.Process(target = schedule__, args = ()).start()
    bot.polling(none_stop=True, interval=0)

'''@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, "ghbdtn")
    #print(message.chat.id, message.chat.username)
    #print(f"[{generate_r2d2()}](tg://user&id={str(message.chat.id)})")'''