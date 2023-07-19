import pymysql
from Return import company_id, returnTerm
from config import *
import time


async def buyp(message):
    term = int(returnTerm(company_id(message.chat.id)))
    t = round(time.time())
    termseconds = term - t
    if termseconds > 0:
        termdays = round(termseconds / 86400)
        if termdays < 1:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
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
    # if PAYMENTS_TOKEN.split(':')[1] == 'TEST':
    #     await bot.send_message(message.chat.id, "Тестовый платеж!!!", reply_markup=types.ReplyKeyboardRemove())
    # else:
    await bot.send_message(message.chat.id, "Подписка", reply_markup=types.ReplyKeyboardRemove())

    await bot.send_invoice(message.chat.id,
                           title="Подписка на бота",
                           description="Активация подписки на бота на 30 дней",
                           provider_token=PAYMENTS_TOKEN,
                           currency="rub",
                           photo_url="https://sun9-10.userapi.com/impg/MBjV1vDCbSLAn6k8kVfySoVF9xf6rxCutiyqgQ/ZbWH1gcHGLg.jpg?size=908x509&quality=96&sign=ca5ac8a23d0421d4c40fbdcd0a07bcf2&type=album",
                           photo_width=416,
                           photo_height=234,
                           photo_size=416,
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="one-month-subscription",
                           payload="test-invoice-payload")


async def pre_checkout_queryp(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


async def successful_paymentp(message: types.Message):
    print("SUCCESSFUL PAYMENT:")
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")
    compid = company_id(message.chat.id)
    oldTerm = int(returnTerm(compid))
    newTerm = oldTerm + paymenAmount if oldTerm > time.time() else time.time() + paymenAmount
    Temp(newTerm, compid)

    await bot.send_message(message.chat.id, f"Вы успешно приобрели подписку на {paymenAmount // 86400} дней.")


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
