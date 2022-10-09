import threading
from config import *
from commands import startc, helpc, mycompanyc, settingc, bot_messagec
from Return import main_page
from Check_Bd import checkbd


def mainf():
    @bot.message_handler(commands=['start'])
    def start(message):
        startc(message)

    @bot.message_handler(commands=['help'])
    def help(message):
        helpc(message)

    @bot.message_handler(commands=['main'])
    def main(message):
        main_page(message.chat.id, 'Главная страница.')

    @bot.message_handler(commands=['mycompany'])
    def mycompany(message):
        mycompanyc(message)

    @bot.message_handler(commands=['setting'])
    def setting(message):
        settingc(message)

    @bot.message_handler(content_types=['text'])
    def bot_message(message):
        bot_messagec(message)

    bot.polling(none_stop=True)


def get_data1():
    checkbd()


thr1 = threading.Thread(target=mainf)
thr1.start()
thr2 = threading.Thread(target=get_data1)
thr2.start()
