import telebot
import mongoengine

import multiprocessing
import schedule
import time

from Bot import config
from Bot.dbinstances import User_stud, Question

# Подключение БД MongoDB и бота
bot = telebot.TeleBot(config.TOKEN)

mongoengine.connect(
    db=config.DB_NAME,
    username=config.DB_USER,
    password=config.DB_PASS,
    host=config.DB_HOST,
    port=config.DB_PART
)


def message_send_readiness():
    """
        Отправка ВСЕМ пользователям вопрос о готовности
        ("Я готов", "Я не готов").
    """

    for stud in User_stud.objects():
        if stud.user_status == "stop":
            stud.user_status = "ready"
            stud = send_single_conf(stud)
            stud.save()


@bot.callback_query_handler(lambda call: call.data == config.READY_BTN[1])
def message_end(call):
    """
        Если пользователь нажал "Я не готов",
        то ему приходит сообщение с ожиданием до завтра.
    """

    bot.answer_callback_query(call.id)
    user = User_stud.objects(user_id=call.message.chat.id).first()

    bot.send_message(user.user_id,
                     text=config.NOT_READY_MSG
                     )

    user.user_status = "stop"
    user.save()


def button_makeup(button, keys):
    """
        Функция, чтобы кнопочки располагались в столбики.
    """

    markup = telebot.types.InlineKeyboardMarkup()

    for text_btn, text2_btn, key, key2 in zip(button[::2], button[1::2],
                                              keys[::2], keys[1::2]):
        markup.add(
            telebot.types.InlineKeyboardButton(text=text_btn,
                                               callback_data=key),
            telebot.types.InlineKeyboardButton(text=text2_btn,
                                               callback_data=key2)
        )

    return markup


def send_questions(user):
    """
        Функция отправки вопроса пользователю.
        (слова и возможный перевод в кнопочках)
    """
    arr_number_questions = user.user_number_que
    question = Question.objects(number=arr_number_questions).first()

    message = f" 🍭 Переведи, пожалуйста это слово: ➡ _{question.text}_ ?\n\n"

    buttons = button_makeup(list(question.answers),
                            list(config.BUTTON_ANS.keys()))

    bot.send_message(user.user_id,
                     message,
                     reply_markup=buttons,
                     parse_mode="markdown"
                     )

    user.user_status = "question"
    user.save()
    print(user.user_status)


@bot.callback_query_handler(lambda call: call.data == config.READY_BTN[0])
def button_handler_ready(call):
    """
        Если пользователь ннажал "Я готов",
        то ему отправляются вопросы.
    """

    bot.answer_callback_query(call.id)
    student = User_stud.objects(user_id=call.message.chat.id).first()

    if student.user_status == "ready":
        send_questions(student)


@bot.callback_query_handler(lambda call: call.data in config.BUTTON_ANS)
def button_handler_questions(call):
    """
        Вывод ответа правильно или неправильно ответил пользователь.
    """

    bot.answer_callback_query(call.id)
    user = User_stud.objects(user_id=call.message.chat.id).first()
    number = user.user_number_que
    question = Question.objects(number=number).first()

    if user.user_status == "question":

        user_answer = question.answers[config.BUTTON_ANS[call.data] - 1]
        correct_answer = question.correct_answer

        print(user_answer)
        print(correct_answer)

        if user_answer == correct_answer:
            bot.send_message(call.message.chat.id,
                             text=config.CORRECT_MSG
                             )
        else:
            bot.send_message(call.message.chat.id,
                             text=config.WRONG_MSG
                             )

            user.user_wrong_answer += f"{number} "
            user.save()

    if user.user_count_que == config.PORTION_QUE:
        user.user_status = "stop"
        user.user_count_que = 0

        if user.user_number_que >= config.COUNT_QUE:
            user.user_number_que = 1
        else:
            user.user_number_que += 1

        bot.send_message(call.message.chat.id,
                         text=config.END_MSG
                         )

        user.save()
    else:
        user.user_count_que += 1

        if user.user_number_que >= config.COUNT_QUE:
            user.user_number_que = 1
        else:
            user.user_number_que += 1

        user.save()
        send_questions(user)


def send_single_conf(stud):
    """
        Вопрос о готовности пользователя (ОДНОГО).
    """
    mark_ = telebot.types.InlineKeyboardMarkup()
    mark_.add(telebot.types.InlineKeyboardButton(text=config.READY_BTN[0],
                                                 callback_data=config.READY_BTN[0]))
    mark_.add(telebot.types.InlineKeyboardButton(text=config.READY_BTN[1],
                                                 callback_data=config.READY_BTN[1]))

    message = "Здравствуй, " + stud.user_name + "!\n" + config.START_EVERYDAY_MSG

    bot.send_message(stud.user_id,
                     text="🥳🇬🇧"
                     )
    bot.send_message(stud.user_id,
                     text=message,
                     reply_markup=mark_
                     )

    return stud


@bot.message_handler(commands=["help"])
def help_messages(message):
    """
        Информация о помощи.
    """
    keyboard = telebot.types.InlineKeyboardMarkup()

    button1 = telebot.types.InlineKeyboardButton(
        config.HELP_BUTTON,
        url='telegram.me/k_ira_18')
    keyboard.add(button1)

    bot.send_message(message.chat.id,
                     text=config.HELP_MESSAGE,
                     reply_markup=keyboard
                     )


@bot.message_handler(commands=["info"])
def developers_messages(message):
    """
        Информация о боте и разработчиках.
    """
    keyboard = telebot.types.InlineKeyboardMarkup()

    button1 = telebot.types.InlineKeyboardButton(
        config.HELP_BUTTON,
        url='telegram.me/k_ira_18')
    keyboard.add(button1)

    bot.send_message(message.chat.id,
                     text=config.INFO_MESSAGE,
                     reply_markup=keyboard
                     )


@bot.message_handler(commands=["start"])
def start_registration(message):
    """
        Запись некоторых данных пользователя в бд.
    """

    if not User_stud.objects(user_id=message.chat.id):
        msg = bot.send_message(message.chat.id,
                               text=config.HELLO_MESSAGE
                               )

        bot.register_next_step_handler(msg, name_ask)

    else:
        bot.send_message(message.chat.id,
                         text="А мы уже знакомы 😄"
                         )


def name_ask(message):
    """
        Запись данных в саму базу данных.
    """
    
    if type(message.text) == str:
        user_name = message.text

        stud = User_stud(
            user_id=message.chat.id,
            user_name=user_name,
            user_status="stop",
            user_count_que=0,
            user_number_que=1,
            user_wrong_answer=""
        )
        stud.save()

        bot.send_message(message.chat.id,
                         text="👋 Привет, " + user_name +
                              config.START_REG_MSG
                         )
    else:
        msg = bot.send_message(message.chat.id,
                               text="😔 Прости, я тебя не понимаю,"
                               "попробуй еще раз"
                               )

        bot.register_next_step_handler(msg, name_ask)


@bot.message_handler(commands=["questions"])
def question_handler(message):
    """
        Если слудент захочет ответить на вопросы просто так.
    """

    if User_stud.objects(user_id=message.chat.id):
        stud = User_stud.objects(user_id=message.chat.id).first()
        print(message.chat.id, stud)
        stud.user_status = "ready"
        stud.save()
        send_single_conf(stud)


@bot.message_handler(commands=["tips"])
def tips_handler(message):
    """
        После ответа на вопросы можео вызвать эту команду,
        чтобы узнать верные ответы на неверно отвеченные вопросы.
    """

    user = User_stud.objects(user_id=message.chat.id).first()
    wrong_ans = user.user_wrong_answer.split(" ")

    if len(wrong_ans) - 1:
        message = " 📌 Повтори эти слова, чтобы в следующий" \
                  " раз правильно ответить: \n"

        for i in range(len(wrong_ans) - 1):
            question = Question.objects(number=wrong_ans[i]).first()

            message += f"• *{question.text}* - {question.correct_answer} \n"

        bot.send_message(user.user_id,
                         text=message,
                         parse_mode="markdown"
                         )

        user.user_wrong_answer = ""
        user.save()
    else:
        bot.send_message(user.user_id,
                         text=config.TIPS_MSG,
                         parse_mode="markdown"
                         )


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    """
        Если пользователь прислал просто текст.
    """

    bot.send_message(message.chat.id,
                     text=config.UNDERSTAND_MSG
                     )


def schedule__():
    """
        Время отправки сообщений про готовность.
    """
    schedule.every().day.at("13:00").do(message_send_readiness)

    schedule.every().day.at("20:00").do(tips_handler)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    multiprocessing.Process(target=schedule__, args=()).start()
    bot.polling(none_stop=True, interval=0)
