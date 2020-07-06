import telebot
import config

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=["help"])
def help_messages(message):

    keyboard = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton(
        u'\U0001f525' "Для связи с разработчиком",
        url='telegram.me/k_ira_18')
    keyboard.add(button1)
    bot.send_message(message.chat.id,
                     "1 - Для начала работы нажмите ▶️ /start\n\n"
                     "2 - Если есть вопросы, пиши разработчикам",
                     reply_markup= keyboard)

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)
if __name__ == '__main__':
    bot.polling(none_stop=True)
