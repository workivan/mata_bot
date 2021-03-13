from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import app.config
from app.user import User


class Register(StatesGroup):
    password = State()
    nickname = State()


async def register(message: types.Message):
    if message.chat.id in app.config.USERS:
        await message.reply('Ты уже зарегистрирован!')
    else:
        await message.reply('Введи пароль для продолжения регистрации')
        await Register.password.set()


async def process_password_step(message: types.Message):
    if app.config.PASSWORD == message.text:
        await Register.next()
        await message.reply("Верный пороль. Теперь введи никнейм!")
    else:
        await message.reply('Пороль не тот, ты не можешь войти в чат! Введи пароль снова')


async def process_nickname_step(message: types.Message, state: FSMContext):
    for user_key, user_value in app.config.USERS.items():
        if user_value.nickname == message.text:
            await message.reply("Этот никнейм уже занят. Выбери другой!")
            return
    user_id = message.chat.id
    nickname = message.text
    username = message.chat.username
    app.config.USERS.update({user_id: User(nickname, username, True)})
    await message.reply("Никнейм свободен. Можешь начать общение!")
    await state.finish()


def register_handlers_register(dp: Dispatcher):
    dp.register_message_handler(register, commands=['register'], state="*")
    dp.register_message_handler(process_password_step, state=Register.password)
    dp.register_message_handler(process_nickname_step, state=Register.nickname)