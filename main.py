import asyncio
import logging
import aiohttp
import os

from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token=os.environ['BOT_TOKEN'])
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

async def current_weather():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://api.openweathermap.org/data/2.5/weather?q=London&appid=82ce53fc45d23c243b0e1fc794f64432') as resp:
            response = await resp.read()
            print(response)

@dp.message_handler(commands=['start'])
async def start_cmd(msg: types.Message):
    await msg.answer('Привет я бот, который отслеживает погоду 😉')
    await current_weather()

@dp.message_handler(commands=['help'])
async def help_cmd(msg: types.Message):
    await msg.answer('я бот, который отслеживает погоду 😉')

if __name__ == '__main__':
    executor.start_polling(dp)
