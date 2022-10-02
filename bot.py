import telebot
import pymysql
import config
import time
from telebot import types
item1_1 = types.KeyboardButton('Войти в систему')
bot = telebot.TeleBot(config.TOKEN)
@bot.message_handler(commands=['start'])
def start(message):
    if check(message.chat.id):
        bot.send_message(message.chat.id, "Вы успешно зашли, ожидаем новые заявки")
        main_page()
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(item1_1)
        bot.send_message(message.chat.id, f"Добро пожаловать {message.from_user.first_name}!"
                                          f"\nВойдите, чтобы отслеживать заявки""",
                         parse_mode="html",  reply_markup=markup)
@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.text == 'Войти в систему':
            bot.send_message(message.chat.id, "Введите логин", reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, login_auth)
def login_auth(message):
    global login, id_p, name_p
    login = message.text
    if login == 'Владелец':
        b1 = types.KeyboardButton('Отмена')
        b2 = types.KeyboardButton('Добавить')
        name_p = message.from_user.first_name
        id_p = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(b1, b2)
        bot.send_message(1878972268, f"Добавить пользователя {message.from_user.first_name}?", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Введите пароль")
        bot.register_next_step_handler(message, passw_auth)
def passw_auth(message):
    global passw
    passw = message.text
    hash_object = passw
    passw = hash_object
    try:
        connection = pymysql.connect(
            host='31.31.196.38',
            port = 3306,
            user='u1721556_admin',
            password='Lapik2022.',
            database='u1721556_telegrambot'
            # cursorclass=pymysql.cursors.DictCursor
        )
        print("successfullu connectid...")
        print("#" * 20)
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT companyId FROM companys WHERE login='{login}' and password='{passw}'")
                result = cursor.fetchone()
                if result == None:
                    bot.send_message(message.chat.id, "Данные введены некорректно.")
                else:
                    cursor.execute("INSERT INTO users (name, chatId, status, companyId) VALUES (%s,%s,%s,%s)",
                                   (message.from_user.first_name, message.chat.id, '1', result[0]))
                    connection.commit()
                    cursor.execute(f"SELECT namecompany FROM companys WHERE companyId='{result[0]}'")
                    result2 = cursor.fetchone()
                    bot.send_message(message.chat.id, f"Вы успешно вошли в компанию {result2[0]}.")
                    main_page()
                    print('Пользователь вошёл в систему')
                    print('#' * 20)
        finally:
            print('#')
    except Exception as ex:
        print("Connection refused…")
        print(ex)
# ----- Проверяет авторизован ли пользователь -----
def check(id):
    try:
        connection = pymysql.connect(
            host='31.31.196.38',
            port = 3306,
            user='u1721556_admin',
            password='Lapik2022.',
            database='u1721556_telegrambot'
            # cursorclass=pymysql.cursors.DictCursor
        )
        print("successfullu connectid...")
        print("#" * 20)
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM users WHERE chatId='{id}'")
                result = cursor.fetchone()
                if result == None:
                    return False
                else:
                    return True
        finally:
            print('#')
    except Exception as ex:
        print("Connection refused…")
        print(ex)
def main_page():
    i = 1
    connection = pymysql.connect(
        host='31.31.196.38',
        port=3306,
        user='u1721556_admin',
        password='Lapik2022.',
        database='u1721556_telegrambot'
        # cursorclas=pymysql.cursors.DictCursor
    )
    while i > 0:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM `application` WHERE `id_companys` = '4' and `status` = '0'")
                result = cursor.fetchall()
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM `users` WHERE `companyId` = '4'")
                result2 = cursor.fetchall()
                if len(result) != 0:
                    a = 0
                    while len(result2)>a:
                        b = 0
                        while len(result)>b:
                            bot = telebot.TeleBot(config.TOKEN)
                            apId = result[b][0]
                            if result[b][4] == 'true':
                                comments = 'написать'
                            else:
                                comments = 'Можно звонить'
                            bot.send_message(result2[a][2], f"<b>--- Новая заявка ---</b>\n<b>Имя:</b> {result[b][2]}\n<b>Телефон:</b> {result[b][3]}\n<b>Комментарий:</b> {comments}\n", parse_mode="html")
                            cursor = connection.cursor()
                            cursor.execute(f"UPDATE `application` SET `status` = '1' WHERE `id` = {apId}")
                            connection.commit()
                            b = b + 1
                        a = a + 1
                else:
                    checkOrders(result2)
        finally:
            print('#')
def checkOrders(result2):
    connection = pymysql.connect(
        host='31.31.196.26',
        port=3306,
        user='u1795882_default',
        password='vAV7v5Kvl7ATn7fA',
        database='u1795882_shopballoons'
        # cursorclas=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM `orders` WHERE `status` = '0'")
            result = cursor.fetchall()
            if len(result) != 0:
                a = 0
                while len(result2)>a:
                    b = 0
                    while len(result)>b:
                        bot = telebot.TeleBot(config.TOKEN)
                        orderId = result[b][0]
                        bot.send_message(result2[a][2], f"<b>--- Новый заказ ---</b>\n<b>Имя:</b> {result[b][2]}\n<b>Телефон:</b> {result[b][3]}\n<b>Email:</b> {result[b][4]}\n<b>Сумма:</b> {result[b][5]}р\n<b>Комментарий:</b> {result[b][6]}\n", parse_mode="html")
                        cursor = connection.cursor()
                        cursor.execute(f"UPDATE `orders` SET `status` = '1' WHERE `id` = {orderId}")
                        connection.commit()
                        b = b + 1
                    a = a + 1
    finally:
        connection.close()
        time.sleep(60)
bot.polling(none_stop=True)
