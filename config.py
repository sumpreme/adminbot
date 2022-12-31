from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

host = "37.140.192.240"
user = "u1843020_admin"
password = "Lapik2022."
bd_name = "u1843020_telegrambot"
# host = "37.140.192.240"
# user = "admin"
# password = "admin1234"
# bd_name = "u1843020_telegrambot"
token = "5626641804:AAF_SpZqEP249cBoy1w8vpIJHZRXi9NOqgs"

# Оплата подписки
PRICE = types.LabeledPrice(label="Подписка на 30 дней", amount=99 * 100)  # в копейках (руб)
bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())
PAYMENTS_TOKEN = "390540012:LIVE:29446"
paymenAmount = 2592000 # 30 дней в секундах
