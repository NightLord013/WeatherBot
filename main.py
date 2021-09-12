import logging
import asyncio
import aiohttp
import os
import json

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

storage = MemoryStorage()
bot = Bot(token=os.environ['BOT_TOKEN'])
dp = Dispatcher(bot, storage=storage)

logging.basicConfig(level=logging.INFO)


class IntervalKindChoose(StatesGroup):
    """Группа состояний для выбора частоты и интервала информаирования пользователя"""
    choose_interval = State()
    choose_frequency = State()


async def get_current_weather():
    """Получение текущей погоды по API"""
    async with aiohttp.ClientSession() as session:
        async with session.get(
                'http://api.openweathermap.org/data/2.5/weather?q=Sarmanovo&appid=82ce53fc45d23c243b0e1fc794f64432') as resp:
            response = await resp.read()
            response = json.loads(response)
            return response


async def get_weather(frequency=10 * 1, msg=None):  # добавить during = '2 дня'
    """Интервальная отправка погоды"""
    during = 3
    while during != 0:
        await asyncio.sleep(frequency)
        weather = await get_current_weather()
        await bot.send_message(718160444, text=weather["weather"][0]['main'])
        during = during - 1
    await bot.send_message(718160444, text="Завершено!")


@dp.message_handler(commands=['start'])
async def start_cmd(msg: types.Message):
    """Событие команды /start"""
    keyboard = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton('Запрос текущей погоды', callback_data='request_current_weather'),
    ]
    keyboard.add(*buttons)
    await msg.answer('Привет я бот, который отслеживает погоду 😉', reply_markup=keyboard)


@dp.message_handler(commands=['help'])
async def help_cmd(msg: types.Message):
    """Событие команды /help"""
    await msg.answer('я бот, который отслеживает погоду 😉')


@dp.callback_query_handler(text='request_current_weather')
async def set_interval(msg: types.Message, state: FSMContext):
    """Колбэк на нажитие кнопки запроса погоды. Запрос у пользователя интервала информирования"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = [
        types.KeyboardButton('В течении дня'),
    ]
    keyboard.add(*buttons)
    await bot.send_message(msg["message"]["chat"]["id"], text='В течении скольки дней присылать прогноз?',
                           reply_markup=keyboard)
    await IntervalKindChoose.choose_interval.set()


@dp.message_handler(state=IntervalKindChoose.choose_interval)
async def set_frequency(msg: types.Message, state: FSMContext):
    """Запрос у пользователя частоты информирования"""
    await state.update_data(interval=msg.text)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = [
        types.KeyboardButton('Каждую минуту'),
    ]
    keyboard.add(*buttons)
    await msg.answer('Как часто присылать прогноз погоды?', reply_markup=keyboard)
    await IntervalKindChoose.next()


@dp.message_handler(state=IntervalKindChoose.choose_frequency)
async def finish_set_up(msg: types.Message, state: FSMContext):
    """Отправка информации и сброс состояния"""
    store = await state.get_data()
    await get_weather(msg=msg)


if __name__ == '__main__':
    executor.start_polling(dp)
