from telebot import types

def num_but():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    num = types.KeyboardButton('Отправить номер', request_contact=True)
    kb.add(num)
    return kb
def loc_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    loc = types.KeyboardButton('Отправить локацию', request_location=True)
    kb.add(loc)
    return kb

def exchange(bot, message):
    user_id = message.from_user.id
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Доллар (USD)", callback_data='USD'))
    markup.add(types.InlineKeyboardButton("Евро (EUR)", callback_data='EUR'))
    bot.send_message(user_id, "Выберите валюту для конвертации:", reply_markup=markup)



