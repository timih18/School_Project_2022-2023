import telebot
import schedule
from threading import Thread
from dict import data
from telebot import types
from TOKEN import token


########################################################################################################################
bot = telebot.TeleBot(token)
photo = 'https://media.discordapp.net/attachments/1020346164505219092/1063730044075261983/IMG_20230114_110257_603.jpg'
chat_id = 0


########################################################################################################################
@bot.message_handler(commands=['start'])
def start(message):
    global chat_id
    chat_id = message.chat.id
    markup = types.InlineKeyboardMarkup(row_width=2)
    plant_1 = types.InlineKeyboardButton('Растение 1', callback_data='plant_1')
    plant_2 = types.InlineKeyboardButton('Растение 2', callback_data='plant_2')
    plant_3 = types.InlineKeyboardButton('Растение 3', callback_data='plant_3')
    plant_4 = types.InlineKeyboardButton('Растение 4', callback_data='plant_4')
    plant_5 = types.InlineKeyboardButton('Растение 5', callback_data='plant_5')
    plant_6 = types.InlineKeyboardButton('Растение 6', callback_data='plant_6')
    markup.add(plant_1, plant_2, plant_3, plant_4, plant_5, plant_6)

    text1 = 'Привет! Это бот по уходу за цветами школы 1561.'
    text2 = 'Я буду присылать напоминания о необходимости полить цветы. Также ты можешь написать '
    text3 = '/(номер на горшке), чтобы узнать информацию о растении.'
    text = text1+'\n'+text2+'\n'+text3
    bot.send_photo(chat_id, photo, caption=text, reply_markup=markup)


########################################################################################################################
@bot.message_handler()
def number(message):
    global chat_id
    chat_id = message.chat.id
    if message.text == '/1' or message.text == '/1@sch1561_plants_bot':
        plant1()
    elif message.text == '/2' or message.text == '/2@sch1561_plants_bot':
        plant2()
    elif message.text == '/3' or message.text == '/3@sch1561_plants_bot':
        plant3()
    elif message.text == '/4' or message.text == '/4@sch1561_plants_bot':
        plant4()
    elif message.text == '/5' or message.text == '/5@sch1561_plants_bot':
        plant5()
    elif message.text == '/6' or message.text == '/6@sch1561_plants_bot':
        plant6()


########################################################################################################################
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        if call.data == 'plant_1':
            plant1()
        elif call.data == 'plant_2':
            plant2()
        elif call.data == 'plant_3':
            plant3()
        elif call.data == 'plant_4':
            plant4()
        elif call.data == 'plant_5':
            plant5()
        elif call.data == 'plant_6':
            plant6()
        elif call.data == 'care_person':
            markup = types.InlineKeyboardMarkup(row_width=1)
            done = types.InlineKeyboardButton('Все полито!', callback_data='done')
            markup.add(done)
            text = f'<b>{call.from_user.first_name}</b> польет растения.'
            bot.send_message(chat_id, text, parse_mode='html', reply_markup=markup)
        elif call.data == 'done':
            bot.send_message(chat_id, 'Все растения политы!')


########################################################################################################################
def reminder1():
    markup = types.InlineKeyboardMarkup(row_width=2)
    plant_1 = types.InlineKeyboardButton('Растение 1', callback_data='plant_1')
    plant_2 = types.InlineKeyboardButton('Растение 2', callback_data='plant_2')
    plant_3 = types.InlineKeyboardButton('Растение 3', callback_data='plant_3')
    care_person = types.InlineKeyboardButton('Я полью', callback_data='care_person')
    markup.add(plant_1, plant_2, plant_3, care_person)

    bot.send_photo(chat_id, photo, caption='Нужно полить растения 1, 2 и 3!', reply_markup=markup)


def reminder2():
    markup = types.InlineKeyboardMarkup(row_width=2)
    plant_4 = types.InlineKeyboardButton('Растение 4', callback_data='plant_4')
    plant_5 = types.InlineKeyboardButton('Растение 5', callback_data='plant_5')
    plant_6 = types.InlineKeyboardButton('Растение 6', callback_data='plant_6')
    care_person = types.InlineKeyboardButton('Я полью', callback_data='care_person')
    markup.add(plant_4, plant_5, plant_6, care_person)

    bot.send_photo(chat_id, photo, caption='Нужно полить растения 4, 5 и 6!', reply_markup=markup)


########################################################################################################################
def plant1():
    photo1 = data['1']['pict']
    bot.send_photo(chat_id, photo1, caption=data['1']['name'] + '\n' + data['1']['desc'])


def plant2():
    photo2 = data['2']['pict']
    bot.send_photo(chat_id, photo2, caption=data['2']['name'] + '\n' + data['2']['desc'])


def plant3():
    photo3 = data['3']['pict']
    bot.send_photo(chat_id, photo3, caption=data['3']['name'] + '\n' + data['3']['desc'])


def plant4():
    photo4 = data['4']['pict']
    bot.send_photo(chat_id, photo4, caption=data['4']['name'] + '\n' + data['4']['desc'])


def plant5():
    photo5 = data['5']['pict']
    bot.send_photo(chat_id, photo5, caption=data['5']['name'] + '\n' + data['5']['desc'])


def plant6():
    photo6 = data['6']['pict']
    bot.send_photo(chat_id, photo6, caption=data['6']['name'] + '\n' + data['6']['desc'])


########################################################################################################################
def main():
    schedule.every().monday.at('10:15').do(reminder1)
    schedule.every().tuesday.at('10:15').do(reminder2)
    schedule.every().thursday.at('10:15').do(reminder1)
    schedule.every().friday.at('10:15').do(reminder2)
########################################################################################################################
    # Для примера
    schedule.every(10).minutes.do(reminder1)
    schedule.every(10).minutes.do(reminder2)
########################################################################################################################

    while True:
        schedule.run_pending()


########################################################################################################################
thread = Thread(target=main)
thread.start()
bot.polling(none_stop=True)
