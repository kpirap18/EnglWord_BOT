import telebot
import multiprocessing
import schedule
import config
import time

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
        if stud.user_status == "stop":
            stud.user_status = "ready"
            stud = send_single_conf(stud)
            stud.save()


def message_end(user, call):
    bot.send_message(user.user_id, text="Тогда до завтра! Хорошего дня! 🦄 \n" 
                                        "Буду ждать тебя 🙄")
    user.user_status = "stop"


def parse_questions(user, call):
    bot.send_message(user.user_id, text="Приступим")


def send_single_conf(stud):
    """
        Вопрос о готовности пользователя
    """
    mark_ = telebot.types.InlineKeyboardMarkup()
    mark_.add(telebot.types.InlineKeyboardButton(text=config.READY_BTN[0],
                                                 callback_data=config.READY_BTN[0]))
    mark_.add(telebot.types.InlineKeyboardButton(text=config.READY_BTN[1],
                                                 callback_data=config.READY_BTN[1]))

    bot.send_message(stud.user_id, text="📄")
    bot.send_message(stud.user_id, config.START_EVERYDAY_MSG, reply_markup=mark_)

    return stud


@bot.callback_query_handler(lambda call: call.data in config.READY_BTN)
def call_question(call):
    """
        Вопрсы после нажатии кнопки
    """
    bot.answer_callback_query(call.id, "")

    user = User_stud.objects(user_id=call.message.chat.id).first()

    if user.user_status == "ready":

        if call.data == config.READY_BTN[0]:
            parse_questions(user, call)

        if call.data == config.READY_BTN[1]:
            message_end(user, call)


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

    bot.send_message(message.chat.id,
                     config.HELP_MESSAGE,
                     reply_markup=keyboard)


@bot.message_handler(commands=["info"])
def developers_messages(message):
    """
        Информация о разработчиках
    """
    keyboard = telebot.types.InlineKeyboardMarkup()

    button1 = telebot.types.InlineKeyboardButton(
        config.HELP_BUTTON,
        url='telegram.me/k_ira_18')
    keyboard.add(button1)

    bot.send_message(message.chat.id,
                     config.INFO_MESSAGE,
                     reply_markup=keyboard)


@bot.message_handler(commands=["start"])
def start_registration(message):
    """
        Запись некоторых данных пользователя в бд
    """

    if not User_stud.objects(user_id=message.chat.id):
        msg = bot.send_message(message.chat.id, config.HELLO_MESSAGE)
        bot.register_next_step_handler(msg, name_ask)

    else:
        bot.send_message(message.chat.id, "А мы уже знакомы 😄")


def name_ask(message):
    """
        Запись имени
    """
    
    if type(message.text) == str:
        user_name = message.text

        login = message.chat.username

        if message.chat.username is None:
            login = f"[{generate_r2d2()}](tg://user&id={str(message.chat.id)})"

        stud = User_stud(
            user_id=message.chat.id,
            user_login=login,
            user_name=user_name,
            user_status="stop"
        )
        stud.save()

        bot.send_message(message.chat.id, "👋 Привет, " + user_name +
                                          "! Мы начинаем изучать слова," 
                                          " мой друг!\n\n"
                                          "Каждый день в 13:00 будут приходить вопросы" 
                                          " так что будь готов! 📝")
    else:
        msg = bot.send_message(message.chat.id, "😔 Прости, я тебя не понимаю,"
                                                "попробуй еще раз")
        bot.register_next_step_handler(msg, name_ask)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, "😔 Я не научился еще понимать твои сообщения," 
                                      " поэтому напиши /info или /help " 
                                      "если не знаешь, что делать, я помогу 😉")


def schedule__():
    schedule.every().day.at("16:59").do(message_send_readiness)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    multiprocessing.Process(target=schedule__, args=()).start()
    bot.polling(none_stop=True, interval=0)
