from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from app.config import *


class DataState(StatesGroup):
    text = State()
    password = State()


async def edit_pin_message(message: types.Message):
    for user_key, user_value in USERS.items():
        if user_key == message.chat.id and user_value.is_admin == True:
            await message.reply('Введи сообщние, которое хочешь закрепить')
            await DataState.text.set()
        else:
            await message.reply('Ты не можешь изменять закрепеленное сообщение')


async def process_edit_msg_step(message: types.Message, state: FSMContext):
    global PIN_MESSAGE
    PIN_MESSAGE = str(message.text)
    await message.reply('Ты успешно поменял закрепленное сообщение')
    await state.finish()


async def edit_password(message: types.Message):
    for user_key, user_value in USERS.items():
        if user_key == message.chat.id and user_value.is_admin == True:
            await message.reply('Введи новый пароль')
            await DataState.text.set()
        else:
            await message.reply('Ты не можешь изменять пароль')


async def process_edit_password_step(message: types.Message, state: FSMContext):
    global PASSWORD
    PASSWORD = str(message.text)
    await message.reply('Ты успешно поменял пароль')
    await state.finish()


def register_handlers_data(dp: Dispatcher):
    dp.register_message_handler(edit_pin_message, commands='edit_pin_message', state='*')
    dp.register_message_handler(process_edit_msg_step, state=DataState.text)
    dp.register_message_handler(edit_password, commands='edit_password', state='*')
    dp.register_message_handler(process_edit_password_step, state=DataState.password)
