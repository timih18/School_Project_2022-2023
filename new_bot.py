import telebot
from telebot import types
import schedule
from threading import Thread


bot = telebot.TeleBot('5845845071:AAEbCWvEapCdLRbLI7VUQSQGgyPg_T-bsNE')
data = {'cnt_start': 0}
# todo: проверить работает ли это в разных чатах
# todo: добавить команду /sp
# todo: добавить уведомления для каждого цветка, след удалить изменить кнопку изменнения времени полива
# todo: добавить удаление растения


@bot.message_handler(commands=['start'])
def start(message):
    global data
    if data['cnt_start'] == 0:
        # todo: Сделать двойной словарь для разных чатов
        data['admin_id'] = message.from_user.id
        data['chat_id'] = message.chat.id
        data['cnt_start'] = 1
        data['cnt_plants'] = 0
        data['time_of_feeding'] = 100
        data['time_since_last_feed'] = 0
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
        msg = f'<b>{message.text[1:]}</b>' + '<b>.</b> ' + f'<b>{data[message.text[1:]]["name"]}</b>' + '\n' +\
              'Описание: ' + data[message.text[1:]]['description'] +\
              '\n' + 'Кабинеты: ' + data[message.text[1:]]['rooms']
        bot.send_message(message.chat.id, msg, parse_mode='html')
    if len(message.text) > 18:
        command = message.text[:-17]
        if command[1:] in data:
            msg = f'<b>{command[1:]}</b>' + '<b>.</b> ' + f'<b>{data[command[1:]]["name"]}</b>' + '\n' + \
                  'Описание: ' + data[command[1:]]['description'] + \
                  '\n' + 'Кабинеты: ' + data[command[1:]]['rooms']
            bot.send_message(message.chat.id, msg, parse_mode='html')


def admin(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    time_of_feeding_button = types.InlineKeyboardButton('Изменить время полива', callback_data='time_of_feeding')
    add_plant_button = types.InlineKeyboardButton('Добавить растение', callback_data='add_plant')
    markup.add(time_of_feeding_button, add_plant_button)
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
    msg = bot.send_message(message.chat.id, 'Введи номера кабинетов, в которых будет стоять растение через "/"')
    bot.register_next_step_handler(msg, after_add_plant_3)


def after_add_plant_3(message):
    global data
    data[str(data['cnt_plants'])]['rooms'] = message.text[1:]
    msg = f'Твое растение сохранено под номером {data["cnt_plants"]}. Ты можешь написать /{data["cnt_plants"]},' \
          f' чтобы увидеть подробную информацию о растении.'
    bot.send_message(message.chat.id, msg)


def reminder():
    global data
    bot.send_message(data['chat_id'], 'Надо полить цветы')


def check_time():
    global data
    if data['cnt_start'] > 0:
        data['time_since_last_feed'] += 1
        if data['time_since_last_feed'] == data['time_of_feeding']:
            reminder()
            data['time_since_last_feed'] = 0


def main():
    global data
    schedule.every(1).second.do(check_time)

    while True:
        schedule.run_pending()


thread = Thread(target=main)
thread.start()
bot.polling(none_stop=True)
