import logging
import os

from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token=os.environ['BOT_TOKEN'])
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=['start'])
async def start_cmd(msg: types.Message):
    await msg.answer('Привет я бот, который отслеживает погоду 😉')

@dp.message_handler(commands=['help'])
async def help_cmd(msg: types.Message):
    await msg.answer('я бот, который отслеживает погоду 😉')

if __name__ == '__main__':
    executor.start_polling(dp)