import telebot
import config
import config_init

bot = telebot.TeleBot(config_init.TOKEN)

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
    bot.send_message(message.chat.id,
                     config.DEV_MESSAGE)

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
    bot.polling(none_stop=True)
