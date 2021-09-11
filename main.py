import logging
import asyncio
import aiohttp
import os
import json

from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token=os.environ['BOT_TOKEN'])
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

async def current_weather():
    """Получение текущей погоды по API"""
    async with aiohttp.ClientSession() as session:
        async with session.get('http://api.openweathermap.org/data/2.5/weather?q=Sarmanovo&appid=82ce53fc45d23c243b0e1fc794f64432') as resp:
            response = await resp.read()
            response = json.loads(response)
            return response

async def get_weather(interval=10*1): # добавить during = '2 дня'
    """Интервальная отправка погоды"""
    during = 3
    while during != 0:
        await asyncio.sleep(interval)
        weather = await current_weather()
        await bot.send_message(718160444, text=weather["weather"][0]['main'])
        during = during -1
    await bot.send_message(718160444, text="Завершено!")

@dp.message_handler(commands=['start'])
async def start_cmd(msg: types.Message):
    """Событие команды /start"""
    keyboard = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton('Запрос текущей погоды', callback_data='cur_weather'),
    ]
    keyboard.add(*buttons)
    await msg.answer('Привет я бот, который отслеживает погоду 😉', reply_markup=keyboard)

@dp.message_handler(commands=['help'])
async def help_cmd(msg: types.Message):
    """Событие команды /help"""
    await msg.answer('я бот, который отслеживает погоду 😉')

@dp.callback_query_handler(text='cur_weather')
async def weather_cmd(msg: types.Message):
    """Калбэк на нажитие кнопки запроса погоды"""
    weather = await current_weather()
    # await bot.send_message(718160444, text=weather["weather"][0]['main'])
    await get_weather()


if __name__ == '__main__':
    executor.start_polling(dp)

