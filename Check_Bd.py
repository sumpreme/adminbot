import time
import pymysql
from config import *


def checkbd():
    # ----- Отправка собранных сообщений -----
    def sending(company, mes, id, host1, user1, password1, name, orders):
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
                    cursor.execute(
                        f"SELECT `chatId` FROM `users` WHERE `companyId`='{company}' and `notify`='1'")
                    result1 = cursor.fetchall()
                    if result1 != ():
                        if host1 == '':
                            # ----- Вывод закявки -----
                            cursor.execute(
                                f"UPDATE `application` SET `status`='1' WHERE `id` = '{id}'")
                            connection.commit()
                            for i1 in range(len(result1)):
                                bot.send_message(result1[i1][0], mes, parse_mode="html")
                        else:
                            # ----- Вывод заказа -----
                            try:
                                connection = pymysql.connect(
                                    host=host1,
                                    port=3306,
                                    user=user1,
                                    password=password1,
                                    database=name,
                                    # cursorclass=pymysql.cursors.DictCursor
                                )
                                print("successfullu connectid...")
                                print("#" * 20)
                                try:
                                    with connection.cursor() as cursor:
                                        cursor.execute(
                                            f"UPDATE `{orders}` SET `status`='1' WHERE `id` = '{id}'")
                                        connection.commit()
                                    for i1 in range(len(result1)):
                                        bot.send_message(result1[i1][0], mes, parse_mode="html")
                                finally:
                                    connection.close()
                            except Exception as ex:
                                print("Connection refused…")
                                print(ex)
            finally:
                connection.close()
        except Exception as ex:
            print("Connection refused…")
            print(ex)

    def surveybd(companyid, host, user, password, name, orders, productsOrders):
        try:
            connection = pymysql.connect(
                host=host,
                port=3306,
                user=user,
                password=password,
                database=name,
                # cursorclass=pymysql.cursors.DictCursor
            )
            print("successfullu connectid...")
            print("#" * 20)
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"SELECT `name`, `phone`, `email`, `price`, `delivery`, `id` FROM `{orders}` WHERE `status` = '0'")
                    result = cursor.fetchall()
                    if result != ():
                        for i in range(len(result)):
                            msg = f"<b>--- Новый заказ ---</b>\n" \
                                  f"<b>Имя:</b> {result[i][0]}\n" \
                                  f"<b>Телефон:</b> {result[i][1]}\n" \
                                  f"<b>Email:</b> {result[i][2]}\n" \
                                  f"<b>Сумма:</b> {result[i][3]}\n" \
                                  f"<b>Комментарий:</b> {result[i][4]}"

                            cursor.execute(
                                f"SELECT `name`, `qty` FROM `{productsOrders}` WHERE `id_order` = {result[i][5]}")
                            result1 = cursor.fetchall()
                            if len(result1) != 0:
                                msg += f"\n<b>Заказы:</b>"
                                for j in range(len(result1)):
                                    msg += f"\n<b>·</b> {result1[j][0]} - {result1[j][1]}шт."
                            sending(companyid, msg, result[i][5], host, user, password, name, orders)


            finally:
                connection.close()
        except Exception as ex:
            print("Connection refused… 105")
            print(ex)

    while True:
        # ----- Опрос БД на новые заявки -----
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
                    cursor.execute(f"SELECT `id_companys`, `name`, `phone`, `comment`, `id` FROM `application` WHERE `status`='0'")
                    result = cursor.fetchall()
                    if result != ():
                        for i in range(len(result)):
                            msg = f"<b>--- Новая заявка ---</b>\n" \
                                  f"<b>Имя:</b> {result[i][1]}\n" \
                                  f"<b>Телефон:</b> {result[i][2]}\n" \
                                  f"<b>Комментарий:</b> {result[i][3]}\n"
                            sending(result[i][0], msg, result[i][4], '', '', '', '', '')
            finally:
                connection.close()
        except Exception as ex:
            print("Connection refused…")
            print(ex)
        time.sleep(10)

        # ----- Опрос БД на новые заказы -----
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
                    cursor.execute(
                        f"SELECT `companyId`, `host`, `user`, `bd_password`, `bd_name`, `bd_orders`, `bd_productsOrder` FROM `companys` WHERE `host` != '-'")
                    result = cursor.fetchall()
                    for i in range(len(result)):
                        surveybd(result[i][0], result[i][1], result[i][2], result[i][3], result[i][4], result[i][5],
                                 result[i][6])

            finally:
                connection.close()
        except Exception as ex:
            print("Connection refused…")
            print(ex)
        time.sleep(10)
