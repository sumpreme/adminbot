from multiprocessing import Process

from commands import startc, helpc, mycompanyc, settingc, bot_messagec
from Return import main_page
from Check_Bd import checkbd
from aiogram import executor
from payment import *
from aiogram.types.message import ContentType

def mainik():
    @dp.message_handler(commands=['start'])
    async def start(message):
        await startc(message)


    @dp.message_handler(commands=['help'])
    async def help(message):
        await helpc(message)


    @dp.message_handler(commands=['main'])
    async def main(message):
        await main_page(message.chat.id, 'Главная страница.')


    @dp.message_handler(commands=['mycompany'])
    async def mycompany(message):
        await mycompanyc(message)


    @dp.message_handler(commands=['setting'])
    async def setting(message):
        await settingc(message)


    @dp.message_handler(commands=['subscription'])
    async def buy(message):
        await buyp(message)


    @dp.message_handler(content_types=['text'])
    async def bot_message(message):
        await bot_messagec(message)


    @dp.pre_checkout_query_handler(lambda query: True)
    async def pre_checkout_queryp(pre_checkout_q: types.PreCheckoutQuery):
        await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


    @dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
    async def successful_payment(message):
        await successful_paymentp(message)

    executor.start_polling(dp, skip_updates=False)


def bd_thread():
    checkbd()

if __name__ == '__main__':
    p = Process(target=bd_thread)
    p2 = Process(target=mainik)
    p.start()
    p2.start()
    p2.join()
    p.join()

