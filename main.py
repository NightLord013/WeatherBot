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
        async with session.get('http://api.openweathermap.org/data/2.5/weather?q=Sarmanovo&appid=82ce53fc45d23c243b0e1fc794f64432') as resp:
            response = await resp.read()
            return response

@dp.message_handler(commands=['start'])
async def start_cmd(msg: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton('Запрос текущей погоды', callback_data='cur_weather'),
    ]
    keyboard.add(*buttons)
    await msg.answer('Привет я бот, который отслеживает погоду 😉', reply_markup=keyboard)

@dp.message_handler(commands=['help'])
async def help_cmd(msg: types.Message):
    await msg.answer('я бот, который отслеживает погоду 😉')

@dp.callback_query_handler(text='cur_weather')
async def weather_cmd(msg: types.Message):
    weather = await current_weather()
    await bot.send_message(718160444, text=weather.decode("utf-8"))


if __name__ == '__main__':
    executor.start_polling(dp)
