import telebot
import pymysql
from TOKEN import token

bot = telebot.TeleBot(token)

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
                     'Тебя приветсвует бот для обратной связи от проекта озеленение классов в школе 1561.')
    bot.send_message(message.chat.id,
                     'В своём проекте мы предлагаем решить проблему с недостатком кислорода в кабинетах раставив растения. Но для них нужен уход, поэтому мы сделали telegram-бота,'
                     'который напоминает об уходе за цветочками.')
    bot.send_message(message.chat.id,
                     'Если вы ещё не протестировали нашего бота для помощи в уходе за растениями то вот он https://t.me/sch1561_plants_bot')
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
                     'Какие ПЛЮСЫ нашего проекта вы заметили?')
    bot.register_next_step_handler(message, q2);


def q2(message):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE chats_id set q2 = %s WHERE chat_id=%s", (message.text, message.chat.id))
        connection.commit()
    bot.send_message(message.chat.id,
                     'Какие НЕДОСТАТКИ нашего проекта вы заметили?')
    bot.register_next_step_handler(message, q3);


def q3(message):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE chats_id set q3 = %s WHERE chat_id=%s", (message.text, message.chat.id))
        connection.commit()
    bot.send_message(message.chat.id,
                     'Спасибо, ваш ответ очень важен для нас.')


bot.polling(none_stop=True)
