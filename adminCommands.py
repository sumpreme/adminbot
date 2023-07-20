import pymysql

from Return import main_page
from config import *
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext


# ----- /setting -----
class AdminSend(StatesGroup):
    send1 = State()
    send2 = State()
    send3 = State()
async def SendMessage(message):
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=bd_name,
            # cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"SELECT `namecompany` FROM `companys` WHERE `companyId` != ''")
                result = cursor.fetchall()
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
                lenMass = len(result)
                pos = 0
                while lenMass >= 2:
                    markup.add(types.KeyboardButton(str(result[pos][0])), types.KeyboardButton(str(result[pos+1][0])))
                    pos += 2
                    lenMass -= 2
                if lenMass == 1:
                    markup.add(types.KeyboardButton(str(result[pos][0])))
                await bot.send_message(message.chat.id, "Выберите компанию", reply_markup=markup)
                await AdminSend.send1.set()
        finally:
            connection.close()
    except Exception as ex:
        print("Connection refused…")
        print(ex)

@dp.message_handler(state=AdminSend.send1)
async def SendMessage_next1(message: types.Message, state: FSMContext):
    if message.text == "/main":
        await main_page(message.chat.id, "Главная страница")
        await state.finish()
    else:
        try:
            connection = pymysql.connect(
                host=host,
                port=3306,
                user=user,
                password=password,
                database=bd_name,
                # cursorclass=pymysql.cursors.DictCursor
            )
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"SELECT `companyId` FROM `companys` WHERE `namecompany` = '{message.text}'")
                    result1 = cursor.fetchone()
                    cursor.execute(
                        f"SELECT `name` FROM `users` WHERE `companyId` = '{result1[0]}'")
                    result = cursor.fetchall()
                    if result == ():
                        await state.finish()
                        await main_page(message.chat.id, 'В этой компании нет пользователей')
                    else:
                        global adminSendIdCompany
                        adminSendIdCompany = result1[0]
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
                        lenMass = len(result)
                        pos = 0
                        while lenMass >= 2:
                            markup.add(types.KeyboardButton(str(result[pos][0])), types.KeyboardButton(str(result[pos+1][0])))
                            pos += 2
                            lenMass -= 2
                        if lenMass == 1:
                            markup.add(types.KeyboardButton(str(result[pos][0])), types.KeyboardButton("Отправить всем"))
                        else:
                            markup.add(types.KeyboardButton("Отправить всем"))

                        await bot.send_message(message.chat.id, "Выберите имя", reply_markup=markup)
                        await AdminSend.next()
            finally:
                connection.close()
        except Exception as ex:
            print("Connection refused…")
            print(ex)

@dp.message_handler(state=AdminSend.send2)
async def SendMessage_next2(message: types.Message, state: FSMContext):
    if message.text == "/main":
        await main_page(message.chat.id, "Главная страница")
        await state.finish()
    else:
        global adminSendName
        adminSendName = message.text
        await bot.send_message(message.chat.id, "Введите текст сообщения", reply_markup=types.ReplyKeyboardRemove())
        await AdminSend.next()

@dp.message_handler(state=AdminSend.send3)
async def SendMessage_next3(message: types.Message, state: FSMContext):
    if message.text == "/main":
        await main_page(message.chat.id, "Главная страница")
        await state.finish()
    else:
        global adminSendName
        if adminSendName == "Отправить всем":
            try:
                connection = pymysql.connect(
                    host=host,
                    port=3306,
                    user=user,
                    password=password,
                    database=bd_name,
                    # cursorclass=pymysql.cursors.DictCursor
                )

                try:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            f"SELECT `chatId` FROM `users` WHERE `companyId`='{adminSendIdCompany}'")
                        result1 = cursor.fetchall()
                        for i1 in range(len(result1)):
                            await bot.send_message(result1[i1][0], message.text, parse_mode="html")
                        await state.finish()
                        await main_page(message.chat.id, 'Сообщение отправлено.')
                finally:
                    connection.close()
            except Exception as ex:
                print("Connection refused… 61")
                print(ex)
        else:
            try:
                connection = pymysql.connect(
                    host=host,
                    port=3306,
                    user=user,
                    password=password,
                    database=bd_name,
                    # cursorclass=pymysql.cursors.DictCursor
                )
                try:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            f"SELECT `chatId` FROM `users` WHERE `companyId` = '{adminSendIdCompany}' and `name` = '{adminSendName}'")
                        result = cursor.fetchone()
                        await bot.send_message(result[0], message.text)
                        await state.finish()
                        await main_page(message.chat.id, 'Сообщение отправлено.')
                finally:
                    connection.close()
            except Exception as ex:
                print("Connection refused…")
                print(ex)
