import telebot
import ast
from telebot import types
import schedule
from threading import Thread
from TOKEN import token

bot = telebot.TeleBot(token)
file = open('data.txt', 'r')
lines = file.readlines()
data = ast.literal_eval(lines[0])
file.close()
plant = ''


@bot.message_handler(commands=['start'])
def start(message):
    global data
    if message.chat.id not in data:
        data_new = {'cnt_plants': 0, 'admin_id': message.from_user.id}
        data[message.chat.id] = data_new
    markup = types.InlineKeyboardMarkup(row_width=1)
    admin_button = types.InlineKeyboardButton('Настройка бота', callback_data='admin')
    markup.add(admin_button)
    text_start = 'Привет! Это бот по уходу за цветами школы 1561. Для настройки нажми на кнопку. ' \
                 'Список команд:' + '\n' + '~ /admin для настройки бота' + '\n' + '~ /list для вывода списка растений' \
                 + '\n' '~ /(номер растения) для вывода информации о растении' + '\n' + '<b>Важно!</b> Чтобы удалить ' \
                                                                                        'бота из чата, очистите все ' \
                                                                                        'данные, с помощью /admin => ' \
                                                                                        '"Очистить данные".'
    bot.send_message(message.chat.id, text_start, parse_mode='html', reply_markup=markup)
    update_data(data)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global data
    if call.message:
        if call.from_user.id == data[call.message.chat.id]['admin_id']:
            if call.data == 'admin':
                admin(call.message)
            elif call.data == 'add_plant':
                add_plant(call.message)
            elif call.data == 'change_time':
                change_time(call.message)
            elif call.data == 'delete_plant':
                delete_plant(call.message)
            elif call.data == 'delete_all':
                delete_all(call.message)
            elif call.data == 'yes_delete':
                after_delete_all(call.message)
            elif call.data == 'change_irrigating':
                change_irrigating(call.message)
        else:
            bot.send_message(call.message.chat.id, 'Ты не администратор этого бота!')


@bot.message_handler()
def text(message):
    global data
    if message.text == '/admin' or message.text == '/admin@sch1561_plants_bot':
        if message.from_user.id == data[message.chat.id]['admin_id']:
            admin(message)
        else:
            bot.send_message(message.chat.id, 'Ты не администратор этого бота!')
    if message.text[1:] in data[message.chat.id]:
        msg = f'<b>{message.text[1:]}</b>' + '<b>.</b> ' + f'<b>{data[message.chat.id][message.text[1:]]["name"]}</b>' \
              + '\n' + 'Поливать каждые ' + str(data[message.chat.id][message.text[1:]]['time_of_feeding']) + \
              ' дня/дней' + '\n' + 'Опрыскивать листья каждые ' + \
              str(data[message.chat.id][message.text[1:]]['time_of_irrigating']) + ' дня/дней' + '\n' + 'Описание: ' + \
              data[message.chat.id][message.text[1:]]['description'] + '\n' + 'Кабинеты: ' + \
              data[message.chat.id][message.text[1:]]['rooms']
        bot.send_message(message.chat.id, msg, parse_mode='html')
    if len(message.text) > 20:
        command = message.text[:-19]
        if command[1:] in data[message.chat.id]:
            msg = f'<b>{command[1:]}</b>' + '<b>.</b> ' + f'<b>{data[message.chat.id][command[1:]]["name"]}</b>' + \
                  '\n' + 'Поливать каждые ' + str(data[message.chat.id][command[1:]]['time_of_feeding']) + ' дня/дней' \
                  + '\n' + 'Опрыскивать листья каждые ' + str(data[message.chat.id][command[1:]]['time_of_irrigating'])\
                  + ' дня/дней' + '\n' + 'Описание: ' + data[message.chat.id][command[1:]]['description'] + '\n' + \
                  'Кабинеты: ' + data[message.chat.id][command[1:]]['rooms']
            bot.send_message(message.chat.id, msg, parse_mode='html')
    if message.text == '/list' or message.text == '/list@sch1561_plants_bot':
        if data[message.chat.id]['cnt_plants'] > 0:
            text_msg = ''
            for i in range(1, data[message.chat.id]['cnt_plants']+1):
                text_msg = text_msg + str(i) + '. ' + f'<b>{data[message.chat.id][str(i)]["name"]}</b>' + '\n'
            bot.send_message(message.chat.id, text_msg, parse_mode='html')
        else:
            bot.send_message(message.chat.id, 'Ты не добавил не одного растения!')


def admin(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    add_plant_button = types.InlineKeyboardButton('Добавить растение', callback_data='add_plant')
    change_time_button = types.InlineKeyboardButton('Изменить время полива', callback_data='change_time')
    delete_plant_button = types.InlineKeyboardButton('Удалить растение', callback_data='delete_plant')
    delete_all_button = types.InlineKeyboardButton('Очистить данные', callback_data='delete_all')
    change_irrigating_button = types.InlineKeyboardButton('Изменить время орошения', callback_data='change_irrigating')
    markup.add(add_plant_button, delete_plant_button, change_time_button, change_irrigating_button, delete_all_button)
    bot.send_message(message.chat.id, 'Что ты хочешь сделать?', reply_markup=markup)


def add_plant(message):
    msg = bot.send_message(message.chat.id, 'Введи название растения через "/".')
    bot.register_next_step_handler(msg, after_add_plant)


def after_add_plant(message):
    global data
    data_plant = {'name': message.text[1:]}
    msg = bot.send_message(message.chat.id, 'Теперь введи краткое описание через "/".')
    bot.register_next_step_handler(msg, after_add_plant_2)
    data[message.chat.id]['cnt_plants'] += 1
    data[message.chat.id][str(data[message.chat.id]['cnt_plants'])] = data_plant
    update_data(data)


def after_add_plant_2(message):
    global data
    data[message.chat.id][str(data[message.chat.id]['cnt_plants'])]['description'] = message.text[1:]
    msg = bot.send_message(message.chat.id, 'Раз в сколько дней присылать уведомления о поливе? Введи число через "/".')
    bot.register_next_step_handler(msg, after_add_plant_3)
    update_data(data)


def after_add_plant_3(message):
    global data
    data[message.chat.id][str(data[message.chat.id]['cnt_plants'])]['time_of_feeding'] = int(message.text[1:])
    data[message.chat.id][str(data[message.chat.id]['cnt_plants'])]['time_since_feed'] = 0
    msg = bot.send_message(message.chat.id, 'Раз в сколько дней ты будешь опрыскивать листья? Введи число через "/".')
    bot.register_next_step_handler(msg, after_add_plant_4)
    update_data(data)


def after_add_plant_4(message):
    global data
    data[message.chat.id][str(data[message.chat.id]['cnt_plants'])]['time_of_irrigating'] = int(message.text[1:])
    data[message.chat.id][str(data[message.chat.id]['cnt_plants'])]['time_since_irrigating'] = 0
    msg = bot.send_message(message.chat.id, 'Введи номера кабинетов, в которых будет стоять растение через "/".')
    bot.register_next_step_handler(msg, after_add_plant_5)
    update_data(data)


def after_add_plant_5(message):
    global data
    data[message.chat.id][str(data[message.chat.id]['cnt_plants'])]['rooms'] = message.text[1:]
    msg = f'Твое растение сохранено под номером {data[message.chat.id]["cnt_plants"]}. Ты можешь написать ' \
          f'/{data[message.chat.id]["cnt_plants"]}, чтобы увидеть подробную информацию о растении.'
    bot.send_message(message.chat.id, msg)
    update_data(data)


def change_time(message):
    msg = bot.send_message(message.chat.id, 'Введи через "/" номер растения, для которого хочешь изменить время '
                                            'полива.')
    bot.register_next_step_handler(msg, after_change_time)


def after_change_time(message):
    global plant
    plant = message.text[1:]
    msg = bot.send_message(message.chat.id, 'Теперь введи новое время полива через "/".')
    bot.register_next_step_handler(msg, after_change_time_2)
    update_data(data)


def after_change_time_2(message):
    global data, plant
    data[message.chat.id][plant]['time_of_feeding'] = int(message.text[1:])
    data[message.chat.id][plant]['time_since_feed'] = 0
    bot.send_message(message.chat.id, 'Время полива изменено.')
    update_data(data)


def delete_plant(message):
    msg = bot.send_message(message.chat.id, 'Введи через "/" номер растения, которое хочешь удалить.')
    bot.register_next_step_handler(msg, after_delete_plant)


def after_delete_plant(message):
    global data
    elem = message.text[1:]
    for i in range(int(elem), data[message.chat.id]['cnt_plants']):
        data[message.chat.id][str(i)] = data[message.chat.id][str(i+1)]
    data[message.chat.id].pop(str(data[message.chat.id]['cnt_plants']))
    data[message.chat.id]['cnt_plants'] -= 1
    bot.send_message(message.chat.id, 'Растение удалено. Номера растений, стоящих после него изменены. Напиши /list, '
                                      'чтобы увидеть новые номера растений.')
    update_data(data)


def delete_all(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    yes_button = types.InlineKeyboardButton('Да', callback_data='yes_delete')
    markup.add(yes_button)
    bot.send_message(message.chat.id, 'Ты точно хочешь удалить все данные?', reply_markup=markup)


def after_delete_all(message):
    global data
    data.pop(message.chat.id)
    bot.send_message(message.chat.id, 'Данные удалены.')
    update_data(data)


def change_irrigating(message):
    msg = bot.send_message(message.chat.id, 'Введи через "/" номер растения, для которого хочешь изменить время '
                                            'опрыскивания.')
    bot.register_next_step_handler(msg, after_change_irrigating)


def after_change_irrigating(message):
    global plant
    plant = message.text[1:]
    msg = bot.send_message(message.chat.id, 'Теперь введи новое время опрыскивания через "/".')
    bot.register_next_step_handler(msg, after_change_irrigating_2)


def after_change_irrigating_2(message):
    global data, plant
    data[message.chat.id][plant]['time_of_irrigating'] = int(message.text[1:])
    data[message.chat.id][plant]['time_since_irrigating'] = 0
    bot.send_message(message.chat.id, 'Время опрыскивания изменено.')
    update_data(data)


def update_data(dictionary):
    strings = open('data.txt', 'r').readlines()
    strings.pop(0)
    with open('data.txt', 'w') as document:
        document.writelines(strings)
        document.write(str(dictionary))
    document.close()


def reminder():
    global data
    for key in data:
        for i in range(1, data[key]['cnt_plants'] + 1):
            if 'time_since_feed' in data[key][str(i)]:
                if data[key][str(i)]['time_of_feeding'] == data[key][str(i)]['time_since_feed']:
                    msg = f'Надо полить <b>{data[key][str(i)]["name"]}</b> (номер {i}).'
                    bot.send_message(key, msg, parse_mode='html')
                    data[key][str(i)]['time_since_feed'] = 0
                else:
                    data[key][str(i)]['time_since_feed'] += 1
            if 'time_since_irrigating' in data[key][str(i)]:
                if data[key][str(i)]['time_of_irrigating'] == data[key][str(i)]['time_since_irrigating']:
                    msg = f'Надо опрыснуть листья <b>{data[key][str(i)]["name"]}</b> (номер {i}).'
                    bot.send_message(key, msg, parse_mode='html')
                    data[key][str(i)]['time_since_irrigating'] = 0
                else:
                    data[key][str(i)]['time_since_irrigating'] += 1
            update_data(data)


def main():
    schedule.every(1).days.at('10:15').do(reminder)
    schedule.every(1).second.do(reminder)

    while True:
        schedule.run_pending()


thread = Thread(target=main)
thread.start()
bot.polling(none_stop=True)
