import telebot
from telebot import types
import schedule
from threading import Thread
import time

bot = telebot.TeleBot('5845845071:AAEbCWvEapCdLRbLI7VUQSQGgyPg_T-bsNE')
data = {}
# todo: проверить работает ли это в разных чатах
cnt_start = 0
cnt_plants = 0


@bot.message_handler(commands=['start'])
def start(message):
    global data
    data['cnt_start'] = 0
    if data['cnt_start'] == 0:
        # todo: Сделать двойной словарь для разных чатов
        data['admin_id'] = message.from_user.id
        data['chat_id'] = message.chat.id
        data['cnt_start'] = 1
        data['cnt_plants'] = 0
    markup = types.InlineKeyboardMarkup(row_width=1)
    admin_button = types.InlineKeyboardButton('Настройка бота', callback_data='admin')
    markup.add(admin_button)
    text_start = 'Привет! Это бот по уходу за цветами школы 1561. Для настройки нажми на кнопку. ' \
                 'Для последующей настройки напиши /admin.'
    bot.send_message(message.chat.id, text_start, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global data
    if call.message:
        if call.data == 'admin':
            if call.from_user.id == data['admin_id']:
                admin(call.message)
            else:
                bot.send_message(call.message.chat.id, 'Ты не администратор этого бота!')
        elif call.data == 'time_of_feeding':
            if call.from_user.id == data['admin_id']:
                time_of_feeding(call.message)
            else:
                bot.send_message(call.message.chat.id, 'Ты не администратор этого бота!')
        elif call.data == 'add_plant':
            if call.from_user.id == data['admin_id']:
                add_plant(call.message)
            else:
                bot.send_message(call.message.chat.id, 'Ты не администратор этого бота!')


@bot.message_handler()
def text(message):
    if message.text == '/admin' or message.text == '/admin@testBot435364Bot':
        admin(message)
    if message.text[1:] in data:
        msg = message.text[1:] + '. ' + data[message.text[1:]]['name'] + '\n' + data[message.text[1:]]['description']
        bot.send_message(message.chat.id, msg)
    if len(message.text) > 18:
        command = message.text[:-17]
        if command[1:] in data:
            msg = command[1:] + '. ' + data[command[1:]]['name'] + '\n' + data[command[1:]]['description']
            bot.send_message(message.chat.id, msg)


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
    data['time_of_feeding'] = int(message.text[1:])


def add_plant(message):
    msg = bot.send_message(message.chat.id, 'Введи название растения через "/"')
    bot.register_next_step_handler(msg, after_add_plant)


def after_add_plant(message):
    global data
    data_plant = {'name': message.text[1:]}
    msg = bot.send_message(message.chat.id, 'Теперь введи краткое описание через "/"')
    bot.register_next_step_handler(msg, after_add_plant_2)
    data['cnt_plants'] += 1
    data[str(data['cnt_plants'])] = data_plant


def after_add_plant_2(message):
    global data
    data[str(data['cnt_plants'])]['description'] = message.text[1:]
    bot.send_message(message.chat.id, f'Описание сохранено. Твое растение сохранено под номером {data["cnt_plants"]}. '
                                      f'Ты можешь написать /{data["cnt_plants"]},'
                                      f' чтобы увидеть подробную информацию о растении.')


def reminder():
    global data
    bot.send_message(data['chat_id'], 'Надо полить цветы')


def main():
    global data
    # todo: Сделать без time.sleep + возможность повторной смены времени полива
    time.sleep(30)
    time_feed = data['time_of_feeding']
    schedule.every(time_feed).days.do(reminder)
    # Для примера
    schedule.every(time_feed).seconds.do(reminder)

    while True:
        schedule.run_pending()


thread = Thread(target=main)
thread.start()
bot.polling(none_stop=True)
