from config import *
from telebot import types
import pymysql
from Variables import item1_2, item1_1
from Return import main_page


# ----- Вход в систему -----
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
    passw = message.text
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=bd_name,
            # cursorclass=pymysql.cursors.DictCursor
        )
        print("successfullu connectid...")
        print("#" * 20)
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT `companyId` FROM `companys` WHERE `login`='{login}' and `password`='{passw}'")
                result = cursor.fetchone()
                if result == None:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    markup.add(item1_1, item1_2)
                    bot.send_message(message.chat.id, "Данные введены некорректно.", reply_markup=markup)
                else:
                    cursor.execute("INSERT INTO `users` (`name`, `chatId`, `status`, `companyId`) VALUES (%s,%s,%s,%s)",
                                   (message.from_user.first_name, message.chat.id, '1', result[0]))
                    connection.commit()
                    cursor.execute(f"SELECT `namecompany` FROM `companys` WHERE `companyId`='{result[0]}'")
                    result2 = cursor.fetchone()
                    main_page(message.chat.id, f"Вы успешно вошли в компанию {result2[0]}.\n\n"
                                               f"Сейчас ничего нет. Ждём новую заявку)")
                    print('Пользователь вошёл в систему')
                    print('#' * 20)
        finally:
            connection.close()
    except Exception as ex:
        print("Connection refused…")
        print(ex)