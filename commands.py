import pymysql
from check import check
from Return import main_page, name_company, company_id, number_status
from Variables import *
from config import *
from auth import login_auth


# ----- /start -----
def startc(message):
    if check(message.chat.id):
        main_page(message.chat.id, f"Вы уже в компании {name_company(company_id(message.chat.id))}")
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(item1_1, item1_2)
        bot.send_message(message.chat.id, f"Добро пожаловать {message.from_user.first_name}!"
                                          f"\nВы можете посмотреть все ваши заказы или статистику, собранную для Вас!",
                         parse_mode="html", reply_markup=markup)


# ----- /help -----
def helpc(message):
    if check(message.chat.id):
        if number_status(message.chat.id) == 3:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(help1)
            bot.send_message(message.chat.id, "Ты что беспомощный?", parse_mode="html", reply_markup=markup)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            markup.add(help2, help3, help1)
            bot.send_message(message.chat.id, "Помощь", parse_mode="html", reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(item1_1, item1_2)
        bot.send_message(message.chat.id, "На данный момент вам не доступны команды.\nВойдите в систему.",
                         parse_mode="html")


# ----- /mycompany -----
def mycompanyc(message):
    if check(message.chat.id):
        bot.send_message(message.chat.id, f"Вы в компании {name_company(company_id(message.chat.id))}")
    else:
        bot.send_message(message.chat.id, "Войдите в систему")


# ----- /setting -----
def settingc(message):
    if check(message.chat.id):
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
                    cursor.execute(f"SELECT `notify` FROM `users` WHERE `chatId`='{message.chat.id}'")
                    result = cursor.fetchone()
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                    if result[0] == 1:
                        markup.add(but_sett_1, button5)
                    else:
                        markup.add(but_sett_2, button5)
                    bot.send_message(message.chat.id, "Настройки", reply_markup=markup)
                    bot.register_next_step_handler(message, setting1)
            finally:
                connection.close()
        except Exception as ex:
            print("Connection refused…")
            print(ex)


def setting1(message):
    if message.text == 'Уведомления: «вкл.»':
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
                    cursor.execute(f"UPDATE `users` SET notify = '0' WHERE `chatId`='{message.chat.id}'")
                    connection.commit()
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                    markup.add(but_sett_2, button5)
                    bot.send_message(message.chat.id, "Уведомления о заказах отключены", reply_markup=markup)
                    bot.register_next_step_handler(message, setting1)
            finally:
                connection.close()
        except Exception as ex:
            print("Connection refused…")
            print(ex)
    elif message.text == 'Уведомления: «выкл.»':
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
                    cursor.execute(f"UPDATE `users` SET notify = '1' WHERE `chatId`='{message.chat.id}'")
                    connection.commit()
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                    markup.add(but_sett_1, button5)
                    bot.send_message(message.chat.id, "Уведомления о заказах включены", reply_markup=markup)
                    bot.register_next_step_handler(message, setting1)
            finally:
                connection.close()
        except Exception as ex:
            print("Connection refused…")
            print(ex)
    elif message.text == 'На главную':
        main_page(message.chat.id, 'Главная страница')

def bot_messagec(message):
    if message.text == 'Войти в систему':
        if check(message.chat.id):
            main_page(message.chat.id, f"Вы уже в компании {name_company(company_id(message.chat.id))}")
        else:
            bot.send_message(message.chat.id, "Введите логин", reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, login_auth)
    elif message.text == 'Информация':
        bot.send_message(message.chat.id, f"Войдите в систему, чтобы начать использовать бота.\n"
                                          f"Если Вы первый раз у нас, напишите <b>@eBurkoff</b>"
                                          f"\nЕсли возникли трудности, всегда можете написать команду /help",
                         parse_mode="html")
    elif check(message.chat.id):
        if message.text == 'Заказы':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            markup.add(button1, button2, button3, button4, button5)
            bot.send_message(message.chat.id, f"Вы открыли вкладку с заказами", reply_markup=markup)
        elif message.text == 'На главную':
            main_page(message.chat.id, "Вы вернулись на главную.")
        elif message.text == 'Вернуть клавиатуру':
            main_page(message.chat.id, "Главная страница.")
        elif message.text == 'Сообщить об ошибке':
            bot.send_message(message.chat.id, "Подробно опишите вашу проблему",
                             reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, report_1)
        elif message.text == 'Предложения по улучшению':
            bot.send_message(message.chat.id, "Подробно опишите вашу проблему",
                             reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, proposal_1)
        elif message.text == 'Заявки':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            markup.add(but_applications_all, but_applications_expectation)
            bot.send_message(message.chat.id, f"Вы открыли вкладку с заявками", reply_markup=markup)
