import telebot
import config
import parse
import pytz

film_list = parse.parse()
P_TIMEZONE = pytz.timezone(config.TIMEZONE)
TIMEZONE_COMMON_NAME = config.TIMEZONE_COMMON_NAME
genre = ''
producer = ''

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id ,
        'Приветствую тебя.\n' +
        'Этот бот поможет выбрать фильмы из списка 1000 фильмов.\n' +
        'Вам нужно выбрать жанр.\n' +
        'Для этого нажмите /genre.\n' +
        'Затем можно выбрать фильм по имени режиссера\n' +
        'Для получения информации о работе бота нажмите /help.'
    )


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(
        message.chat.id ,
        '1) Для выбора жанров нажмите /genre.\n' +
        '2) Дальше вам предложат на выбор несколько жанров, нажмите на интересующий вас.\n' +
        '3) Дальше вам предложат на выбор несколько режиссеров, нажмите на интересующего вас.\n' +
        '4) Вам придет сообщение с названием и картинкой фильма, также укажется некоторая информация о фильме '
    )


@bot.message_handler(commands=['genre'])
def genre_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('Драма' , callback_data='genre_btn1'))
    keyboard.row(
        telebot.types.InlineKeyboardButton('Триллер' , callback_data='genre_btn2'))
    keyboard.row(
        telebot.types.InlineKeyboardButton('Комедия' , callback_data='genre_btn3'))
    keyboard.row(
        telebot.types.InlineKeyboardButton('Семейное' , callback_data='genre_btn4'))
    keyboard.row(
        telebot.types.InlineKeyboardButton('Приключения' , callback_data='genre_btn5'))
    keyboard.row(
        telebot.types.InlineKeyboardButton('Анимация' , callback_data='genre_btn6'))
    keyboard.row(
        telebot.types.InlineKeyboardButton('Любой жанр' , callback_data='genre_btn7'))
    bot.send_message(
        message.chat.id ,
        'Выберите жанр:\n' ,
        reply_markup=keyboard
    )


@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    data = query.data
    if data.startswith('genre_btn'):
        bot.answer_callback_query(query.id)
        get_genre_callback(query)
    if data.startswith('producer_btn'):
        bot.answer_callback_query(query.id)
        get_producer_callback(query)


def get_genre_callback(query):
    bot.answer_callback_query(query.id)
    send_genre_result(query.message , query.data[9:])


def send_genre_result(message , ex_code):
    global genre
    bot.send_chat_action(message.chat.id , 'typing')
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('Фрэнк Дарабонт' , callback_data='producer_btn1'))
    keyboard.row(
        telebot.types.InlineKeyboardButton('Гай Ричи' , callback_data='producer_btn2'))
    keyboard.row(
        telebot.types.InlineKeyboardButton('Джеймс Кэмерон' , callback_data='producer_btn3'))
    keyboard.row(
        telebot.types.InlineKeyboardButton('Питер Фаррелли' , callback_data='producer_btn4'))
    keyboard.row(
        telebot.types.InlineKeyboardButton('Любой режиссер' , callback_data='producer_btn5'))
    if ex_code == '1':
        genre = 'драма'
        bot.send_message(
            message.chat.id ,
            'Вы выбрали Драму\n' +
            'Выберите Режиссера:\n' ,
            reply_markup=keyboard
        )
    if ex_code == '2':
        genre = 'триллер'
        bot.send_message(
            message.chat.id ,
            'Вы выбрали Триллер\n' +
            'Выберите Режиссера:\n' ,
            reply_markup=keyboard
        )
    if ex_code == '3':
        genre = 'комедия'
        bot.send_message(
            message.chat.id ,
            'Вы выбрали Комедию\n' +
            'Выберите Режиссера:\n' ,
            reply_markup=keyboard
        )
    if ex_code == '4':
        genre = 'семейный'
        bot.send_message(
            message.chat.id ,
            'Вы выбрали Семейное\n' +
            'Выберите Режиссера:\n' ,
            reply_markup=keyboard
        )
    if ex_code == '5':
        genre = 'приключения'
        bot.send_message(
            message.chat.id ,
            'Вы выбрали Приключение\n' +
            'Выберите Режиссера:\n' ,
            reply_markup=keyboard
        )
    if ex_code == '6':
        genre = 'анимация'
        bot.send_message(
            message.chat.id ,
            'Вы выбрали Анимацию\n' +
            'Выберите Режиссера:\n' ,
            reply_markup=keyboard
        )
    if ex_code == '7':
        bot.send_message(
            message.chat.id ,
            'Вы выбрали Любой жанр\n' +
            'Выберите Режиссера:\n' ,
            reply_markup=keyboard
        )


def get_producer_callback(query):
    bot.answer_callback_query(query.id)
    send_producer_result(query.message , query.data[12:])


def send_producer_result(message , ex_code):
    global genre
    bot.send_chat_action(message.chat.id , 'typing')
    if ex_code == '1':
        producer = 'Фрэнк Дарабонт'
        if genre != '':
            num , film = parse.get_random_movie_of_genre_and_producer(genre , producer , film_list)
        else:
            num , film = parse.get_random_movie_of_producer(producer , film_list)
        if film != None:
            num = 'images/' + str(num) + '.jpeg'
            img = open(num , 'rb')
            bot.send_photo(message.chat.id , img)
            bot.send_message(
                message.chat.id ,
                'Вы выбрали Фрэнка Дарабонта\n\n' +
                'Вы получили фильм: \n' +
                film
            )
        else:
            bot.send_message(
                message.chat.id ,
                'Увы! Такого фильма не нашлось, попробуйте еще раз'
            )
    if ex_code == '2':
        producer = 'Гай Ричи'
        if genre != '':
            num , film = parse.get_random_movie_of_genre_and_producer(genre , producer , film_list)
        else:
            num , film = parse.get_random_movie_of_producer(producer , film_list)
        if film != None:
            num = 'images/' + str(num) + '.jpeg'
            img = open(num , 'rb')
            bot.send_photo(message.chat.id , img)
            bot.send_message(
                message.chat.id ,
                'Вы выбрали Гая Ричи\n\n' +
                'Вы получили фильм: \n' +
                film
            )
        else:
            bot.send_message(
                message.chat.id ,
                'Увы! Такого фильма не нашлось, попробуйте еще раз'
            )
    if ex_code == '3':
        producer = 'Джеймс Кэмерон'
        if genre != '':
            num , film = parse.get_random_movie_of_genre_and_producer(genre , producer , film_list)
        else:
            num , film = parse.get_random_movie_of_producer(producer , film_list)
        if film != None:
            num = 'images/' + str(num) + '.jpeg'
            img = open(num , 'rb')
            bot.send_photo(message.chat.id , img)
            bot.send_message(
                message.chat.id ,
                'Вы выбрали Джейса Кэмерона\n\n' +
                'Вы получили фильм: \n' +
                film
            )
        else:
            bot.send_message(
                message.chat.id ,
                'Увы! Такого фильма не нашлось, попробуйте еще раз'
            )
    if ex_code == '4':
        producer = 'Питер Фаррелли'
        if genre != '':
            num , film = parse.get_random_movie_of_genre_and_producer(genre , producer , film_list)
        else:
            num , film = parse.get_random_movie_of_producer(producer , film_list)
        if film != None:
            num = 'images/' + str(num) + '.jpeg'
            img = open(num , 'rb')
            bot.send_photo(message.chat.id , img)
            bot.send_message(
                message.chat.id ,
                'Вы выбрали Питера Фаррелли\n\n' +
                'Вы получили фильм: \n' +
                film
            )
        else:
            bot.send_message(
                message.chat.id ,
                'Увы! Такого фильма не нашлось, попробуйте еще раз'
            )
    if ex_code == '5':
        if genre != '':
            num , film = parse.get_random_movie_of_genre(genre, film_list)
        else:
            num , film = parse.get_random_movie(film_list)
        if film != None:
            num = 'images/' + str(num) + '.jpeg'
            img = open(num , 'rb')
            bot.send_photo(message.chat.id , img)
            bot.send_message(
                message.chat.id ,
                'Вы выбрали Любой режиссер\n\n' +
                'Вы получили фильм: \n' +
                film
            )
        else:
            bot.send_message(
                message.chat.id ,
                'Увы! Такого фильма не нашлось, попробуйте еще раз'
            )


bot.polling(none_stop=True)
