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
        await message.reply('Вы уже зарегистрированы!')
    else:
        await message.reply('Введите пароль для продолжения регистрации')
        await Register.password.set()


async def process_password_step(message: types.Message, state: FSMContext):
    if app.config.PASSWORD == message.text:
        await Register.next()
        await message.reply("Верный пороль. Теперь введите никнейм!")
    else:
        await message.reply('Пороль не тот, Вы не можете войти в чат! Начните регитрацию заново')
        await state.finish()


async def process_nickname_step(message: types.Message, state: FSMContext):
    for user_key, user_value in await app.config.USERS.items():
        if user_value.nickname == message.text:
            await message.reply("Этот никнейм уже занят. Введите другой!")
            return
    user_id = message.chat.id
    nickname = message.text
    username = message.chat.username
    await app.config.USERS.update({user_id: User(nickname, username, True)})
    await message.reply('''Никнейм свободен! Вы зарегистрированы и можете начать общение.
                        Приятного общения :) Напиши что-нибудь сейчас ;)''')
    await state.finish()


def register_handlers_register(dp: Dispatcher):
    dp.register_message_handler(register, commands=['register'], state="*")
    dp.register_message_handler(process_password_step, state=Register.password)
    dp.register_message_handler(process_nickname_step, state=Register.nickname)
