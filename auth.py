from config import *
from aiogram import types
import pymysql
from Variables import item1_2, item1_1
from Return import main_page
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext


class Auth(StatesGroup):
    login = State()
    authp = State()
# ----- Вход в систему -----
@dp.message_handler(state=Auth.login)
async def login_auth(message):
    global login, id_p, name_p
    login = message.text
    if login == 'Владелец':
        b1 = types.KeyboardButton('Отмена')
        b2 = types.KeyboardButton('Добавить')
        name_p = message.from_user.first_name
        id_p = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(b1, b2)
        await bot.send_message(1878972268, f"Добавить пользователя {message.from_user.first_name}?", reply_markup=markup)
    else:
        await bot.send_message(message.chat.id, "Введите пароль")
        await Auth.next()

@dp.message_handler(state=Auth.authp)
async def passw_auth(message: types.Message, state: FSMContext):
    passw = message.text
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
                cursor.execute(f"SELECT `companyId`, `companyId` FROM `companys` WHERE `login`='{login}' and `password`='{passw}'")
                result = cursor.fetchone()
                if result is None:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    markup.add(item1_1, item1_2)
                    await state.finish()
                    await bot.send_message(message.chat.id, "Данные введены некорректно.", reply_markup=markup)
                else:
                    cursor.execute("INSERT INTO `users` (`name`, `chatId`, `status`, `companyId`) VALUES (%s,%s,%s,%s)",
                                   (message.from_user.first_name, message.chat.id, '1', result[0]))
                    await main_page(message.chat.id, f"Вы успешно вошли в компанию {result[1]}.\n\nСейчас ничего нет. Ждём новую заявку.")
                    print('Пользователь вошёл в систему')
                    print('#' * 20)
                    connection.commit()
                    await state.finish()
        finally:
            connection.close()
    except Exception as ex:
        print("Connection refused…")
        print(ex)
