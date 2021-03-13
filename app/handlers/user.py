from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from app.config import *


class UserState(StatesGroup):
    delete = State()
    add = State()


async def delete_user(message: types.Message):
    for user_key, user_value in USERS.items():
        if user_key == message.chat.id and user_value.is_admin == True:
            await message.answer('Введи никнейм того, кого хочешь удалить')
            await UserState.delete.set()
            return
    await message.answer('Ты не можешь банить пользователей')


async def process_delete_user_step(message: types.Message, state: FSMContext):
    for user_key, user_value in USERS.items():
        if user_value.nickname == message.text:
            user_value.banned = True
            await message.answer('Пользователь удален!' + str(user_value.login))
            await bot.send_message(user_key, 'Ты забанен в чате!')
            await state.finish()
            return
    await message.answer('Человека с таким никнеймом нет в чате. Повтори попытку')


async def add_user(message: types.Message):
    for user_key, user_value in USERS.items():
        if user_key == message.chat.id and user_value.is_admin == True:
            await message.answer('Введи никнейм того, кого разбанить')
            await UserState.add.set()
            return
    await message.answer('Ты не можешь разбанить пользователей')


async def process_add_user_step(message: types.Message, state: FSMContext):
    for user_key, user_value in USERS.items():
        if user_value.nickname == message.text:
            user_value.banned = False
            await message.answer('Пользователь возвращен!')
            await bot.send_message(user_key, 'Ты раззабанен в чате!')
            await state.finish()
            return
    await message.answer('Человека с таким никнеймом нет в чате. Повтори попытку')


async def pause_mess(message: types.Message):
    if message.chat.id in USERS:
        if USERS.get(message.chat.id).subscription:
            USERS.get(message.chat.id).subscription = False
            await message.answer('Ты отписался от чата')
        else:
            await message.answer('Ты и так уже отписался от чата!')


async def proceed_mess(message: types.Message):
    if message.chat.id in USERS:
        if not USERS.get(message.chat.id).subscription:
            USERS.get(message.chat.id).subscription = True
            await message.answer('Ты вновь в чате!')
        else:
            await message.answer('Ты и так подписан на чат')


def register_handlers_user(dp: Dispatcher):
    dp.register_message_handler(delete_user, commands='delete_user', state='*')
    dp.register_message_handler(process_delete_user_step, state=UserState.delete)
    dp.register_message_handler(add_user, commands='add_user', state='*')
    dp.register_message_handler(pause_mess, commands='pause_chat', state='*')
    dp.register_message_handler(proceed_mess, commands='proceed_chat', state='*')
    dp.register_message_handler(process_add_user_step, state=UserState.add)
