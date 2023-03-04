import telebot
from telebot import types
import schedule
from threading import Thread


bot = telebot.TeleBot('5845845071:AAEbCWvEapCdLRbLI7VUQSQGgyPg_T-bsNE')
data = {'cnt_start': 0, 'cnt_plants': 0}
# todo: добавить команду /sp
# todo: изменить кнопку изменнения времени полива
# todo: добавить удаление растения
# todo: изменить реагирование бота на все сообщения


@bot.message_handler(commands=['start'])
def start(message):
    global data
    if data['cnt_start'] == 0:
        # todo: Сделать двойной словарь для разных чатов
        data['admin_id'] = message.from_user.id
        data['chat_id'] = message.chat.id
        data['cnt_start'] = 1
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
              'Поливать каждые ' + str(data[message.text[1:]]['time_of_feeding']) + ' дня/дней' + '\n' + 'Описание: ' +\
              data[message.text[1:]]['description'] + '\n' + 'Кабинеты: ' + data[message.text[1:]]['rooms']
        bot.send_message(message.chat.id, msg, parse_mode='html')
    if len(message.text) > 18:
        command = message.text[:-17]
        if command[1:] in data:
            msg = f'<b>{command[1:]}</b>' + '<b>.</b> ' + f'<b>{data[command[1:]]["name"]}</b>' + '\n' + \
                  'Поливать каждые ' + str(data[command[1:]]['time_of_feeding']) + ' дня/дней' + '\n' + 'Описание: ' + \
                  data[command[1:]]['description'] + '\n' + 'Кабинеты: ' + data[command[1:]]['rooms']
            bot.send_message(message.chat.id, msg, parse_mode='html')


def admin(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    add_plant_button = types.InlineKeyboardButton('Добавить растение', callback_data='add_plant')
    markup.add(add_plant_button)
    bot.send_message(message.chat.id, 'Что ты хочешь сделать?', reply_markup=markup)


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
    msg = bot.send_message(message.chat.id, 'Раз в сколько дней присылать уведомления о поливе? Введи число через "/"')
    bot.register_next_step_handler(msg, after_add_plant_3)


def after_add_plant_3(message):
    global data
    data[str(data['cnt_plants'])]['time_of_feeding'] = int(message.text[1:])
    data[str(data['cnt_plants'])]['time_since_feed'] = 0
    msg = bot.send_message(message.chat.id, 'Введи номера кабинетов, в которых будет стоять растение через "/"')
    bot.register_next_step_handler(msg, after_add_plant_4)


def after_add_plant_4(message):
    global data
    data[str(data['cnt_plants'])]['rooms'] = message.text[1:]
    msg = f'Твое растение сохранено под номером {data["cnt_plants"]}. Ты можешь написать /{data["cnt_plants"]},' \
          f' чтобы увидеть подробную информацию о растении.'
    bot.send_message(message.chat.id, msg)


def reminder():
    for i in range(1, data['cnt_plants']+1):
        if 'time_since_feed' in data[str(i)]:
            if data[str(i)]['time_of_feeding'] == data[str(i)]['time_since_feed']:
                msg = f'Надо полить <b>{data[str(i)]["name"]}</b> (номер {i})'
                bot.send_message(data['chat_id'], msg, parse_mode='html')
                data[str(i)]['time_since_feed'] = 0
            else:
                data[str(i)]['time_since_feed'] += 1


def main():
    global data
    schedule.every(1).seconds.do(reminder)

    while True:
        schedule.run_pending()


thread = Thread(target=main)
thread.start()
bot.polling(none_stop=True)
