import telebot
from telebot import types
import schedule
from threading import Thread
import time

bot = telebot.TeleBot('5845845071:AAEbCWvEapCdLRbLI7VUQSQGgyPg_T-bsNE')
# todo: добавить импорт словаря
data = {}
cnt_start = 0


@bot.message_handler(commands=['start'])
def start(message):
    global data, cnt_start
    data_new = {}
    # todo: проверить работает ли это в разных чатах
    if cnt_start == 0:
        data_new['admin_id'] = message.from_user.id
        cnt_start += 1
    markup = types.InlineKeyboardMarkup(row_width=1)
    admin_button = types.InlineKeyboardButton('Настройка бота', callback_data='admin')
    markup.add(admin_button)
    text_start = 'Привет! Это бот по уходу за цветами школы 1561. Для настройки нажми на кнопку. ' \
                 'Для последующей настройки напиши /admin.'
    bot.send_message(message.chat.id, text_start, reply_markup=markup)
    data[message.chat.id] = data_new


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global data
    if call.message:
        if call.data == 'admin':
            if call.from_user.id == data[call.message.chat.id]['admin_id']:
                admin(call.message)
            else:
                bot.send_message(call.message.chat.id, 'Ты не администратор этого бота!')
        elif call.data == 'time_of_feeding':
            if call.from_user.id == data[call.message.chat.id]['admin_id']:
                time_of_feeding(call.message)
            else:
                bot.send_message(call.message.chat.id, 'Ты не администратор этого бота!')
        elif call.data == 'add_plant':
            if call.from_user.id == data[call.message.chat.id]['admin_id']:
                add_plant(call.message)
            else:
                bot.send_message(call.message.chat.id, 'Ты не администратор этого бота!')


@bot.message_handler()
def text(message):
    if message.text == '/admin' or message.text == '/admin@testBot435364Bot':
        admin(message)


def admin(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    time_of_feeding_button = types.InlineKeyboardButton('Изменить время полива', callback_data='time_of_feeding')
    add_plant_button = types.InlineKeyboardButton('Добавить растение', callback_data='add_plant')
    change_button = types.InlineKeyboardButton('Изменить уже введенное', callback_data='change')
    markup.add(time_of_feeding_button, add_plant_button, change_button)
    bot.send_message(message.chat.id, 'Что ты хочешь сделать?', reply_markup=markup)


def time_of_feeding(message):
    msg = bot.send_message(message.chat.id, 'Как часто присылать уведомления о поливе?' + '\n' +
                           'Напиши время через "/". Например, "/3".')
    bot.register_next_step_handler(msg, after_time_of_feeding)


def after_time_of_feeding(message):
    global data
    bot.send_message(message.chat.id, 'Уведомления будут присылаться каждые ' + message.text[1:] + ' дней')
    data[message.chat.id]['time_of_feeding'] = int(message.text[1:])


# todo: добавить для каждого цветка свой словарь
def add_plant(message):
    msg = bot.send_message(message.chat.id, 'Введи название растения через "/"')
    bot.register_next_step_handler(msg, after_add_plant)


def after_add_plant(message):
    global data
    msg = bot.send_message(message.chat.id, 'Теперь введи краткое описание')
    bot.register_next_step_handler(msg, after_add_plant_2)
    # todo: добавить занесение в словарь
# todo: добавить after_add_plant_2


def reminder():
    global data
    # todo: как определить chat_id
    # bot.send_message(data[], 'Надо полить цветы')


def main():
    global data
    # todo: Сделать без time.sleep + возможность повторной смены времени полива
    time.sleep(30)
    # todo: как определить chat_id
    # time_feed = data[]
    # schedule.every(time_feed).days.do(reminder)
    # Для примера
    # schedule.every(time_feed).seconds.do(reminder)

    while True:
        schedule.run_pending()


thread = Thread(target=main)
thread.start()
bot.polling(none_stop=True)
