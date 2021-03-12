from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from app.config import *

class UserState(StatesGroup):
    delete = State()


async def delete_user(message: types.Message):
    for user_key, user_value in USERS.items():
        if user_key == message.chat.id and user_value.is_admin == True:
            await message.reply('Введи никнейм того, кого хочешь удалить')
            await UserState.delete.set()
        else:
            await message.reply('Ты не можешь банить пользователей')


async def process_delete_user_step(message: types.Message, state: FSMContext):
    for user_key, user_value in USERS.items():
        if user_value.nickname == message.text:
            user_value.banned = True
            await message.answer('Пользователь удален!')
            await bot.send_message(user_key, 'Ты забанен в чате!')
            await state.finish()
            return
    await message.answer('Человека с таким никнеймом нет в чате')


def register_handlers_user(dp: Dispatcher):
    dp.register_message_handler(delete_user, commands='delete_user', state='*')
    dp.register_message_handler(process_delete_user_step, state=UserState.delete)