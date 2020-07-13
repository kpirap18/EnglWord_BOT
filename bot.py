import telebot
import config
import config_init

import datetime
import mongoengine
from random import randint, seed
from mongo_models import User_stud, Question

bot = telebot.TeleBot(config_init.TOKEN)
mongoengine.connect('test')


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

def generate_r2d2():

    #seed(datetime.now())
    return f"R{randint(0, 100)}-D{randint(0, 100)}"

@bot.message_handler(commands=["developers"])
def developers_messages(message):
    bot.send_message(message.chat.id, config.DEV_MESSAGE)

@bot.message_handler(commands=["start"])
def start_registration(message):
    if not User_stud.objects(user_id=message.chat.id):
        User_stud.login = message.chat.username

        if message.chat.username is None:
            User_stud.login = f"[{generate_r2d2()}](tg://user&id={str(message.chat.id)})"


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)
    print(message.chat.id, message.chat.username)
    print(f"[{generate_r2d2()}](tg://user&id={str(message.chat.id)})")


if __name__ == '__main__':
    bot.polling(none_stop=True)
