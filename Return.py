import pymysql
from config import host, user, password, bd_name, bot
from telebot import types
from check import check
from Variables import but_st3_1, but_st3_2, but_st3_3  # , but1, but2, but_applications


# -----  По chat.id возвращает companyId  -----
def company_id(chatid):
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
                cursor.execute(f"SELECT `companyId` FROM `users` WHERE `chatId`='{chatid}'")
                result = cursor.fetchone()
                return result[0]
        finally:
            connection.close()
    except Exception as ex:
        print("Connection refused…")
        print(ex)


# ----- Возвращает имя компании по id -----
def name_company(id):
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
                cursor.execute(f"SELECT `namecompany` FROM `companys` WHERE `companyId`='{id}'")
                result = cursor.fetchone()
                return result[0]
        finally:
            connection.close()
    except Exception as ex:
        print("Connection refused…")
        print(ex)


# ----- Статус по chatId -----
def number_status(id):
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
                cursor.execute(f"SELECT `status` FROM `users` WHERE `chatId`='{id}'")
                result = cursor.fetchone()
                return result[0]
        finally:
            connection.close()
    except Exception as ex:
        print("Connection refused…")
        print(ex)


# ----- Возврат на главную -----
def main_page(id, mes):
    if check(id):
        if number_status(id) == 3:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
            markup.add(but_st3_1, but_st3_2, but_st3_3)
            bot.send_message(id, f"{mes}", parse_mode="html", reply_markup=markup)
        else:
            # markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            # markup.add(but1, but2, but_applications)
            # bot.send_message(id, f"{mes}", parse_mode="html", reply_markup=markup)
            bot.send_message(id, mes, parse_mode="html", reply_markup=types.ReplyKeyboardRemove())
