"""
    Файл с данными для бота.

    - регистрационные данные баз данных
    - данные для подключения бота
    - тексты сообщений, для упрощения чтения кода
"""

HELP_MESSAGE = "❓ Не знаешь, что делать ❓ \n\n" \
               "Мы поможем ⤵ \n\n" \
               "1 - Для начала работы нажмите ▶️ /start\n\n" \
               "2 - Для получения инфрмации про бота нажми ❔ /info\n\n" \
               "3 - Для ответов на вопросы (в любое время) нажми /questions\n\n" \
               "4 - Для получения подсказок после ответа на вопросы нажми /tips\n\n" \
               "5 - Если есть вопросы, пиши разработчикам ⬇ "

HELLO_MESSAGE = "👋 Привет, я - бот для изучения слов по английскому языку. 🇬🇧" \
                "Надеюсь тебе понравится, слова легкие, поэтому не переживай" \
                ", а пока начнем! 💪\n\n" \
                "Скажи мне, пожалуйста, как тебя зовут?"

INFO_MESSAGE = "📎 Этот бот предназначен для изучения английских слов. 🇬🇧 \n\n" \
               "📎 Сообщение о готовности будет приходить каждый день " \
               "в 13:00, так что будьте готовы! 📝\n\n" \
               "💫 Разработчики данного бота: \n" \
               "🔹 Козлова Ирина (@k_ira_18)"

START_EVERYDAY_MSG = "🇬🇧 Готов ли ты, мой милый друг, ответить на пару вопросов " \
                     "от меня и показать, что ты знаешь английские слова?"

NOT_READY_MSG = "Тогда до завтра! Хорошего дня! 🦄 \n" \
                "Буду ждать тебя 🙄"

END_MSG = "А ты молодец, хорошо справляешься! \n До завтра! 🤗"
CORRECT_MSG = "Правильно 😀, так держать! 🟢"
WRONG_MSG = "Эх 😔, к сожалению, неправильно 🔴"

UNDERSTAND_MSG = "😔 Я не научился еще понимать твои сообщения," \
                 " поэтому напиши /info или /help " \
                 "если не знаешь, что делать, я помогу 😉"

TIPS_MSG = "🤔 У меня есть 2 предположения: \n\n" \
           "• Либо ты сегодня молодец и все верно ответил. ☺\n" \
           "• Либо ты сегодня не отвечал. 🙄\n\n" \
           "Прости, я пока не умею это определять 😔"

START_REG_MSG = "! Мы начинаем изучать слова," \
                " мой друг!\n\n" \
                "Каждый день в 13:00 будут приходить вопросы" \
                " так что будь готов! 📝"

HELP_BUTTON = " Для связи с разработчиком 💬"
READY_BTN = [" Я готов! ✅ ", "Я не готов! ❌"]
BUTTON_ANS = {"1️⃣": 1, "2️⃣": 2, "3️⃣": 3, "4️⃣": 4}
PORTION_QUE = 4
COUNT_QUE = 15

DB_NAME = "test"
DB_USER = "ira"
DB_PASS = "1234"
DB_HOST = "localhost"
DB_PART = 27017
TOKEN = '1374290854:AAEYk6MgHcwGkOXwX_6uNgNEXdaQhsq6k1o'

