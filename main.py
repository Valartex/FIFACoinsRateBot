import telebot
from telebot import types
from parser_db import get_coins_list
from users_log_db import add_log_record, get_users_count

bot = telebot.TeleBot('key')
# bot = telebot.TeleBot('key') # ключ от тестового бота


# Предложение выбрать платформу с выводом клавиатуры
def platform_choice(message, question):
    kb_markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
    kb_markup.add('PC', 'PS', 'XBOX')
    msg = bot.send_message(message.from_user.id, question, reply_markup = kb_markup)
    bot.register_next_step_handler(msg, process_platform_step)


# Предложение выбрать количество монет
def coins_count_choice(message, question, platform):
    kb_markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, row_width = 5)
    kb_markup.add('50K', '60K', '70K', '80K', '90K', '100K', '200K', '300K', '400K', '500K', '600K', '700K', '800K',
                  '900K', '1000K', '1500K', '2000K')
    msg = bot.send_message(message.from_user.id, question, reply_markup = kb_markup)
    bot.register_next_step_handler(msg, process_quantity_step, platform)


# Обработка введённого периода дат для отчёта по количеству пользователей
def show_users_count(message):
    user_message = message.text.strip()
    space = user_message.find(' ')

    start_date = user_message[:space]
    end_date = user_message[space:].strip()

    users_count = get_users_count(start_date, end_date)

    bot.send_message(message.from_user.id, users_count)


# Handle '/start'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    platform_choice(message, 'What platform do you need coins for?')

    # запись действия в лог
    user_id = message.from_user.id
    user_name = message.from_user.username
    add_log_record({'user_id': user_id, 'user_name': user_name, 'event': 'start'})


# Handle '/help'
@bot.message_handler(commands=['help'])
def send_help(message):
    kb_markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
    kb_markup.add('/start')

    bot.send_message(message.from_user.id,
                     f'I help to find FIFA coins at the lowest price.\n\n'
                     'Just press <b>/start</b> and follow the prompts.\n'
                     'Or send me a message in the format: <b>game_platform_name</b> <b>amount_of_coins</b>.\n'
                     'For example: <b>ps 100k</b>.\n'
                     'Game platform name: <b>pc, ps, xbox</b>.\n\n'
                     'Please note that the price in the bot may differ from the price on the website, since the price is influenced by some factors, for example, the geographic location of the buyer.\n\n'
                     'Support: @FIFA_CRBS',
                     parse_mode = "HTML", reply_markup = kb_markup)


# Handle '/getuserscount'
@bot.message_handler(commands=['getuserscount'])
def get_report_period(message):
    msg = bot.send_message(message.from_user.id, 'For what period do you need a report (e.g.: 2021-07-01 2021-07-02)?')
    bot.register_next_step_handler(msg, show_users_count)


def validate_user_message(user_message):
    parsing_parameters = {}

    space = user_message.find(' ')

    platform = user_message[:space]
    quantity = user_message[space:].replace('k', '000', 2).strip()

    if platform in ['pc', 'ps', 'xbox'] and quantity.isdigit:
        parsing_parameters['platform'] = platform
        parsing_parameters['quantity'] = quantity

    return parsing_parameters


# Обработка всех произвольных текстовых сообщений
# В частности, здесь обрабатывается ручной ввод параметров поиска в формате "[имя_платформы] [количество_монет]"
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    user_message = message.text.lower().strip()
    parsing_parameters = validate_user_message(user_message)

    if len(parsing_parameters) == 2:
        show_coins_list(message, parsing_parameters)
    elif user_message not in ['help', 'start', '/getuserscount']:
        bot.send_message(message.from_user.id, 'Type /start or /help.')


# Обработка inline-запросов
@bot.inline_handler(lambda query: len(query.query) > 3)
def get_inline_message(inline_query):
    try:
        user_message = inline_query.query.lower().strip()
        parsing_parameters = validate_user_message(user_message)

        if len(parsing_parameters) == 2:
            coins_list = get_coins_list(parsing_parameters)

            links = ''
            for link in coins_list:
                links = links + '\n\n' + link

            inline_result = types.InlineQueryResultArticle(1, 'Send list to chat...', types.InputTextMessageContent(links, parse_mode = "HTML", disable_web_page_preview = True))

            # r2 = types.InlineQueryResultArticle('2', 'Result2', types.InputTextMessageContent('hi'))
            bot.answer_inline_query(inline_query.id, [inline_result])
    except Exception as e:
        print(e)


# Обработка введённого значения платформы. Если всё правильно, переходим к вводу количества монет
def process_platform_step(message):
    platform = message.text.lower()
    if platform in ['pc', 'ps', 'xbox']:
        coins_count_choice(message, 'How many coins do you need? The value can be any: from 1 or more.', platform)
    else:
        platform_choice(message, 'Unknown platform.\nWhat platform do you need coins for?')


# Обработка введённого количества монет. Если всё правильно, вызываем функцию парсинга
def process_quantity_step(message, platform):
    parsing_parameters = {}

    quantity = message.text.lower().replace('k', '000', 2) # если пользователь указал тысячи буквой k, то меняем её первые 2 вхождения на нули
    if quantity.isdigit():
        parsing_parameters['platform'] = platform
        parsing_parameters['quantity'] = quantity
        show_coins_list(message, parsing_parameters)        
    else:
        coins_count_choice(message, "It doesn't look like a number.\nHow many coins do you need? The value can be any: from 1 or more.")


def show_coins_list(message, parsing_parameters):
    bot.send_message(message.from_user.id, "Here's what the sellers have that are similar to what you were looking for:")
    coins_list = get_coins_list(parsing_parameters)

    links = ''
    for link in coins_list:
        links = links + '\n\n' + link

    kb_markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
    kb_markup.add('/start')

    bot.send_message(message.from_user.id, links, disable_web_page_preview = True, parse_mode = "HTML", reply_markup = kb_markup)

    # запись действия в лог
    user_id = message.from_user.id
    user_name = message.from_user.username
    add_log_record({'user_id': user_id, 'user_name': user_name, 'event': 'show_coins_list'})


bot.polling(none_stop = True, interval = 0)