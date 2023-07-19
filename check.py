import pymysql
from config import host, user, password, bd_name


# ----- Проверяет авторизован ли пользователь -----
def check(id):
    try:
        connection = pymysql.connect(
            host=host,
            port=888,
            user=user,
            password=password,
            database=bd_name,
            # cursorclass=pymysql.cursors.DictCursor
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM `users` WHERE `chatId`='{id}'")
                result = cursor.fetchone()
                if result == None:
                    return False
                else:
                    return True
        finally:
            connection.close()
    except Exception as ex:
        print("Connection refused…")
        print(ex)
