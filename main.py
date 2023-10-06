import telebot, buttons as bt, database as db
from geopy import Nominatim
from forex_python.converter import CurrencyRates
from telebot import types

bot = telebot.TeleBot('6315617308:AAG6E_e5oLDV11urHwzJ3bIie9NyfLIPst8') #ссылка на бота https://t.me/currency_tekhnuikum_bot
c = CurrencyRates()

geolocator = Nominatim(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36')

@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    check_user = db.checker(user_id)
    if check_user:
        bot.send_message(user_id, 'Добро пожаловать!', reply_markup=telebot.types.ReplyKeyboardRemove())
        bt.exchange(bot, message)
    else:
        bot.send_message(user_id, 'Добро пожаловать!\n'
                                'Давайте начнем регистрацию! Введите имя',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_name)
@bot.message_handler(commands=['help'])
def help_message(message):
    user_id = message.from_user.id
    help_text = "Это бот для конвертации валюты. Вы можете использовать следующие команды:\n\n" \
                "/start - начать регистрацию\n" \
                "/help - отобразить это сообщение справки\n" \
                "/exchange - начать процесс конвертации валюты"
    bot.send_message(user_id, help_text)
def get_name(message):
    user_name = message.text
    user_id = message.from_user.id
    bot.send_message(user_id, 'Отлично! Теперь номер', reply_markup=bt.num_but())
    bot.register_next_step_handler(message, get_num, user_name)
def get_num(message, user_name):
    user_id = message.from_user.id
    if message.contact:
        user_num = message.contact.phone_number
        bot.send_message(user_id, 'Супер, теперь локацию!',
                         reply_markup=bt.loc_button())
        bot.register_next_step_handler(message, get_loc, user_name, user_num)
    else:
        bot.send_message(user_id, 'Отправьте номер, используя кнопку!')
        bot.register_next_step_handler(message, get_num, user_name)
def get_loc(message, user_name, user_num):
    user_id = message.from_user.id
    if message.location:
        user_loc = geolocator.reverse(f'{message.location.longitude},'
                                      f'{message.location.latitude}')
        db.register(user_id, user_name, user_num, user_loc)
        bot.send_message(user_id, 'Регистрация успешно завершена!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        bot.send_message(user_id, 'Отправьте локацию, используя кнопку!')
        bot.register_next_step_handler(message, get_loc, user_name, user_num)

@bot.callback_query_handler(func=lambda call: True)
def callback_1(callback):
    user_id = callback.from_user.id
    currency = callback.data
    bot.send_message(user_id, f'Введите сумму для конвертации в {currency}:')
    bot.register_next_step_handler(callback.message, convert_currency, currency)

def convert_currency(message, currency):
    user_id = message.from_user.id
    try:
        amount = float(message.text)
        converted_amount = c.convert('UZS', currency, amount)
        bot.send_message(user_id, f'{amount} UZS равно {converted_amount} {currency}.')
        bt.exchange(bot, message)
    except ValueError:
        bot.send_message(user_id, 'Пожалуйста, введите числовое значение.')

@bot.message_handler(commands=['exchange'])
def exchange_command(message):
    user_id = message.from_user.id
    bt.exchange(bot, message)

bot.polling(none_stop=True)
