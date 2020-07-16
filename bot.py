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
    #seed(datetime.now())
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
    user.save()

def button_makeup(button):
    """
        Кнопки в столбики
    """

    markup = telebot.types.InlineKeyboardMarkup()

    for text_btn, text2_btn in zip(button[::2], button[1::2]):
        markup.add(
            telebot.types.InlineKeyboardButton(text=text_btn, callback_data=text_btn),
            telebot.types.InlineKeyboardButton(text=text2_btn, callback_data=text2_btn)
        )

    return markup


def send_questions(user):
    """
        Функция отправки вопроса пользователю (слова и возможный перевод)
    """

    bot.send_message(user.user_id, text="Приступим!")
    arr_number_questions = 1  # randint(0, config.COUNT_QUE)
    question = Question.objects(number=arr_number_questions).first()
    user.user_number_que = arr_number_questions

    message = f"❓ {question.text}\n\n"
    for button, ans in zip(config.BUTTON_ANS, question.answers):
        message += f"🔸{button}. {ans}\n"

    buttons = button_makeup(list(config.BUTTON_ANS.keys()))

    bot.send_message(user.user_id,
                     message,
                     reply_markup=buttons
                     )

    user.user_status = "question"
    user.save()
    print(user.user_status)

@bot.callback_query_handler(lambda call: call.data == config.READY_BTN[0])
def query_handler_ready(call):
    """
        Высылание вопроса с кнопками тем,
        кто подтвердил готовность отвечать на вопрос.
    """

    bot.answer_callback_query(call.id)
    student = User_stud.objects(user_id=call.message.chat.id).first()

    if student.user_status == "ready":
        send_questions(student)

@bot.callback_query_handler(lambda call: call.data in config.BUTTON_ANS)
def query_handler_questions(call):
    """
        Обработка нажатия inline-кнопок с выбором ответа студентом.
    """

    bot.answer_callback_query(call.id)
    user = User_stud.objects(user_id=call.message.chat.id).first()
    num = user.user_number_que
    question = Question.objects(number=num).first()

    if user.user_status == "question":

        user_answer = call.message.text.split("\n")[config.BUTTON_ANS[call.data]+1][4:]
        correct_answer = question.correct_answer

        print(user_answer)
        print(correct_answer)

        if user_answer == correct_answer:
            bot.send_message(call.message.chat.id, "Правильно 😀, так держать! 🟢")
        else:
            bot.send_message(call.message.chat.id, "Эх 😔, к сожалению, неправильно 🔴")

    if user.user_count_que == config.PORTION_QUE:
        user.user_status = "stop"
        user.user_count_que = 0
        user.user_number_que = 0
        user.save()
        bot.send_message(call.message.chat.id, "Сейчас вопросов нет, спасибо," 
                                               " что ответил!")
    else:
        user.user_count_que += 1
        user.save()
        send_questions(user)

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
            user_status="stop",
            user_count_que=0,
            user_number_que=0
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

@bot.message_handler(commands=["question"])
def question_handler(message):
    if User_stud.objects(user_id=message.chat.id):
        stud = User_stud.objects(user_id=message.chat.id).first()
        print(message.chat.id, stud)
        stud.user_status = "ready"
        stud.save()
        send_single_conf(stud)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, "😔 Я не научился еще понимать твои сообщения," 
                                      " поэтому напиши /info или /help " 
                                      "если не знаешь, что делать, я помогу 😉")


def schedule__():
    schedule.every().day.at("13:00").do(message_send_readiness)
    schedule.every().day.at("16:00").do(message_send_readiness)
    schedule.every().day.at("20:00").do(message_send_readiness)
    schedule.every().day.at("23:25").do(message_send_readiness)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    multiprocessing.Process(target=schedule__, args=()).start()
    bot.polling(none_stop=True, interval=0)
