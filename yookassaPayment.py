import asyncio
import time
import pymysql
import json
from yookassa import Configuration, Payment

from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

from Return import company_id, returnTerm, main_page
from config import *

# ----- choiceTerm -----
class ChoiceTerm(StatesGroup):
    term1 = State()

async def buyp(message):
    term = int(returnTerm(company_id(message.chat.id)))
    t = round(time.time())
    termseconds = term - t
    if termseconds > 0:
        termdays = round(termseconds / 86400)
        if termdays < 1:
            markup = types.ReplyKeyboard(resize_keyboard=True)
            markup.add(types.KeyboardButton('Продлить подписку'))
            await bot.send_message(message.chat.id, f"До окончания подписки осталось меньше суток", reply_markup=markup)
        else:
            if termdays % 10 == 1:
                mes = "день"
            elif termdays % 10 in [2, 3, 4]:
                mes = "дня"
            else:
                mes = "дней"
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton('Продлить подписку'))
            await bot.send_message(message.chat.id, f"До окончания подписки осталось {termdays} {mes}.", reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('Купить подписку'))
        await bot.send_message(message.chat.id, f"У Вас кончилась подписка.", reply_markup=markup)

async def buyp1(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    markup.add(types.KeyboardButton("30"), types.KeyboardButton("100"), types.KeyboardButton("365"))
    msg = ""
    for i in range(len(paymentList[0])):
        msg += f"\n{paymentList[0][i]} дней - {paymentList[1][i]} рублей"
    await bot.send_message(message.chat.id, f"Выберите количество дней:{msg}", reply_markup=markup)
    await ChoiceTerm.term1.set()

@dp.message_handler(state=ChoiceTerm.term1)
async def buyp2(message: types.Message, state: FSMContext):
    await state.finish()
    if message.text == str(paymentList[0][0]):
        await buyPay(message.chat.id, paymentList[0][0], index=0)
    elif message.text == str(paymentList[0][1]):
        await buyPay(message.chat.id, paymentList[0][1], index=1)
    elif message.text == str(paymentList[0][2]):
        await buyPay(message.chat.id, paymentList[0][2], index=2)



async def buyPay(id, term, index):
    await bot.send_message(id, f"Подписка на {term} дней.", reply_markup=types.ReplyKeyboardRemove())
    imageURL = ["https://webirai.ru/tetegramBot/99.jpg", "https://webirai.ru/tetegramBot/299.jpg", "https://webirai.ru/tetegramBot/1099.jpg"]

    compId = company_id(id)

    payment = Payment.create({
        "amount": {
            "value": paymentList[1][index],
            "currency": "RUB"
        },
        "payment_method_data": {
            "type": "bank_card"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://www.example.com/return_url"
        },
        "capture": True,
        "description": "Подписка на бота",
        "metadata": {
            "term": f"{term}"
        }
    })

    payment_data = json.loads(payment.json())
    payment_id = payment_data['id']
    payment_url = (payment_data['confirmation'])['confirmation_url']
    payment_term = (payment_data['metadata'])['term']
    await bot.send_photo(id, imageURL[index], f"Оплатите по ссылке:{payment_url}", reply_markup=types.ReplyKeyboardRemove())

    async def check_payment(payment_id):
        payment = json.loads((Payment.find_one(payment_id)).json())
        while payment['status'] == 'pending':
            payment = json.loads((Payment.find_one(payment_id)).json())
            await asyncio.sleep(3)

        if payment['status'] == 'succeeded':
            print("SUCCSESS RETURN")
            print(payment)

            # payment_data = json.loads(payment.json())
            # payment_term = (payment_data['metadata'])['term']

            return True
        else:
            print("BAD RETURN")
            print(payment)
            return False

    if await check_payment(payment_id):
        oldTerm = int(returnTerm(compId))
        newTerm = oldTerm + term * paymenAmount if oldTerm > time.time() else time.time() + term * paymenAmount
        Temp(newTerm, compId)
        await main_page(id, "Подписка успешно оплачена.")
    else:
        await main_page(id, "Ошибка оплаты.")



def Temp(newTemp, id):
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
                cursor.execute(
                    f"UPDATE `companys` SET `term`='{newTemp}' WHERE `companyId` = '{id}'")
                named_tuple = time.localtime()
                time_string = time.strftime("%d/%m/%Y, %H:%M:%S", named_tuple)
                cursor.execute(
                    f"UPDATE `companys` SET `lastpayment`='{time_string}' WHERE `companyId` = '{id}'")
                cursor.execute(
                    f"UPDATE `companys` SET `notify_pay`='0' WHERE `companyId` = '{id}'")
                connection.commit()
        finally:
            connection.close()
    except Exception as ex:
        print("Connection refused…")
        print(ex)
