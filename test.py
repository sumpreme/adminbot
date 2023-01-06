from config import *
import asyncio
from aiogram.utils.keyboard import ReplyKeyboardBuilder


@dp.message_handler(commands=['main'])
async def main(message: types.Message):
    markup = ReplyKeyboardBuilder()
    markup.add(types.KeyboardButton("lol"))
    await bot.send_message(message.chat.id, "pppp")


executor.start_polling(dp, skip_updates=False)
