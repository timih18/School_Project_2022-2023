import telebot
import pymysql

bot = telebot.TeleBot('6242867193:AAFGTiIdP0Acjnm4FAMWgC164-R4GAidyKk')

try:
    connection = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='root',
        database='plants',
        cursorclass=pymysql.cursors.DictCursor
    )
    print('succesfully connected...')
except Exception as ex:
    print('Connection refused...')
    print(ex)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
                     'Тебя приветсвуте бот для обратной связи от проекта оезеленение классов в школе 1561.')
    bot.send_message(message.chat.id,
                     'Ответь на несколько вопрсов. Помоги сделать наш проект лучше.')
    bot.send_message(message.chat.id,
                     'Оцените пользу нашего проекта от 1 до 10.')
    with connection.cursor() as cursor:
        cursor.execute("REPLACE INTO `chats_id` (chat_id) VALUES (%s)", (message.chat.id))
        connection.commit()
    bot.register_next_step_handler(message, q1);


def q1(message):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE chats_id set q1 = %s WHERE chat_id=%s", (message.text, message.chat.id))
        connection.commit()
    bot.send_message(message.chat.id,
                     'Какие ПЛЮСЫ нашего проекта вы заметили.')
    bot.register_next_step_handler(message, q2);


def q2(message):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE chats_id set q2 = %s WHERE chat_id=%s", (message.text, message.chat.id))
        connection.commit()
    bot.send_message(message.chat.id,
                     'Какие МИНУСЫ нашего проекта вы заметили.')
    bot.register_next_step_handler(message, q3);


def q3(message):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE chats_id set q3 = %s WHERE chat_id=%s", (message.text, message.chat.id))
        connection.commit()


connection.close()
bot.polling(none_stop=True)
