import pymysql

import adminCommands
from check import check
from Return import main_page, name_company, company_id, number_status
from Variables import *
from config import *
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

from auth import Auth
from yookassaPayment import buyp1
#from payment import buyp1


# ----- /start -----
async def startc(message):
    if check(message.chat.id):
        await main_page(message.chat.id, f"Вы уже в компании {name_company(company_id(message.chat.id))}")
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(item1_1, item1_2)
        await bot.send_message(message.chat.id, f"Добро пожаловать {message.from_user.first_name}!"
                                          f"\nВы можете посмотреть все ваши заказы или статистику, собранную для Вас!",
                         parse_mode="html", reply_markup=markup)


# ----- /help -----
async def helpc(message):
    if check(message.chat.id):
        if number_status(message.chat.id) == 3:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(help1)
            await bot.send_message(message.chat.id, "Ты что беспомощный?", parse_mode="html", reply_markup=markup)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            markup.add(help2, help3, help1)
            await bot.send_message(message.chat.id, "Помощь", parse_mode="html", reply_markup=markup)
            await bot.send_message(message.chat.id, "Друзья! Тестовый период бота для сбора заказов и заявок окончен. Стоимость подписки 99р/30дней.\n\nПо всем вопросам - webirai.studio@gmail.com", parse_mode="html")
            await bot.send_message(message.chat.id, "Проверить подписку /subscription", parse_mode="html")
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(item1_1, item1_2)
        await bot.send_message(message.chat.id, "На данный момент вам не доступны команды.\nВойдите в систему.",
                         parse_mode="html")


# ----- /mycompany -----
async def mycompanyc(message):
    if check(message.chat.id):
        await bot.send_message(message.chat.id, f"Вы в компании {name_company(company_id(message.chat.id))}")
    else:
        await bot.send_message(message.chat.id, "Войдите в систему")


# ----- /setting -----
class Setting(StatesGroup):
    s1 = State()

async def settingc(message):
    if check(message.chat.id):
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
                    cursor.execute(f"SELECT `notify` FROM `users` WHERE `chatId`='{message.chat.id}'")
                    result = cursor.fetchone()
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                    if result[0] == 1:
                        markup.add(but_sett_1, button5)
                    else:
                        markup.add(but_sett_2, button5)
                    await bot.send_message(message.chat.id, "Настройки", reply_markup=markup)
                    await Setting.s1.set()
            finally:
                connection.close()
        except Exception as ex:
            print("Connection refused…")
            print(ex)

@dp.message_handler(state=Setting.s1)
async def setting1(message: types.Message, state: FSMContext):
    if message.text == 'Уведомления: «вкл.»':
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
                    cursor.execute(f"UPDATE `users` SET notify = '0' WHERE `chatId`='{message.chat.id}'")
                    connection.commit()
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                    markup.add(but_sett_2, button5)
                    await bot.send_message(message.chat.id, "Уведомления о заказах отключены", reply_markup=markup)
            finally:
                connection.close()
        except Exception as ex:
            print("Connection refused…")
            print(ex)
    elif message.text == 'Уведомления: «выкл.»':
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
                    cursor.execute(f"UPDATE `users` SET notify = '1' WHERE `chatId`='{message.chat.id}'")
                    connection.commit()
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                    markup.add(but_sett_1, button5)
                    await bot.send_message(message.chat.id, "Уведомления о заказах включены", reply_markup=markup)
            finally:
                connection.close()
        except Exception as ex:
            print("Connection refused…")
            print(ex)
    elif message.text == 'На главную':
        await state.finish()
        await main_page(message.chat.id, 'Главная страница')

async def bot_messagec(message):
    if message.text == 'Войти в систему':
        if check(message.chat.id):
            await main_page(message.chat.id, f"Вы уже в компании {name_company(company_id(message.chat.id))}")
        else:
            await bot.send_message(message.chat.id, "Введите логин", reply_markup=types.ReplyKeyboardRemove())
            await Auth.login.set()
    elif message.text == 'Информация':
        await bot.send_message(message.chat.id, f"Войдите в систему, чтобы начать использовать бота.\n"
                                          f"Если Вы первый раз у нас, напишите <b>@eBurkoff</b>"
                                          f"\nЕсли возникли трудности, всегда можете написать команду /help",
                         parse_mode="html")
    elif check(message.chat.id):
        if message.text == 'Заказы':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            markup.add(button1, button2, button3, button4, button5)
            await bot.send_message(message.chat.id, f"Вы открыли вкладку с заказами", reply_markup=markup)
        elif message.text == 'На главную':
            await main_page(message.chat.id, "Вы вернулись на главную.")
        elif message.text == 'Сообщить об ошибке':
            await bot.send_message(message.chat.id, "Подробно опишите вашу проблему",
                             reply_markup=types.ReplyKeyboardRemove())
            #bot.register_next_step_handler(message, report_1)
        elif message.text == 'Предложения по улучшению':
            await bot.send_message(message.chat.id, "Подробно опишите вашу проблему",
                             reply_markup=types.ReplyKeyboardRemove())
            #bot.register_next_step_handler(message, proposal_1)
        elif message.text == 'Заявки':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            markup.add(but_applications_all, but_applications_expectation)
            await bot.send_message(message.chat.id, f"Вы открыли вкладку с заявками", reply_markup=markup)
        elif message.text in ["Продлить подписку", "Купить подписку"]:
            await buyp1(message)
        elif number_status(message.chat.id) == 3:
            if message.text == 'Отправить сообщение':
                await adminCommands.SendMessage(message)
