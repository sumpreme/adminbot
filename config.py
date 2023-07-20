from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from yookassa import Configuration

# host = "31.31.196.38"
# user = "u1721556_admin"
# password = "Lapik2022."
# bd_name = "u1721556_telegrambot"
# host = "37.140.192.240"
# user = "admin"
# password = "admin1234"
# bd_name = "u1843020_telegrambot"
# ........... Основа ............
host = "93.183.75.73"
user = "telegram_usr"
password = "Lapik2023."
bd_name = "telegram"
# ...............................
token = "5626641804:AAF_SpZqEP249cBoy1w8vpIJHZRXi9NOqgs"
#token = "5471405708:AAEw83oAsPHAxbEnIxEyG5oWwjjDf4rjqSs"

# Оплата подписки
PRICE = types.LabeledPrice(label="Подписка на 30 дней", amount=99 * 100)  # в копейках (руб)
bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())
PAYMENTS_TOKEN = "390540012:LIVE:29446"
paySize = 1  # сумма одного месяца подписки в рублях
paymenAmount = 84000  # 1 день в секундах
paymentList = [[30, 100, 365], [99, 299, 1099]]

Configuration.account_id = 961979
Configuration.secret_key = "live_D0owMwHU6My8_1kYsMSdfHO9GYFMtPmW_225uXVf-kc"
