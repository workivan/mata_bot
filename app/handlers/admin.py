from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from app.config import *


class AdminState(StatesGroup):
    add = State()
    delete = State()


async def register_admin(message: types.Message):
    if int(message.chat.id) == SUPER_USER_ID:
        await message.reply('Введи никнейм того, кого хочешь сделать администратором')
        await AdminState.add.set()
    else:
        await message.reply('Ты не можешь добавлять новых администраторов')


async def process_add_admin_step(message: types.Message, state: FSMContext):
    for user_key, user_value in USERS.items():
        if user_value.nickname == message.text:
            user_value.is_admin = True
            await message.answer('Новый администратор добавлен!')
            await bot.send_message(user_key, 'Теперь ты администратор!')
            await state.finish()
            return
    await message.answer('Человека с таким никнеймом нет в чате. Повтори попытку')


async def delete_admin(message: types.Message):
    if int(message.chat.id) == SUPER_USER_ID:
        await message.reply('Введи никнейм того, кого хочешь удалить из админстратором')
        await AdminState.delete.set()
    else:
        await message.reply('Ты не можешь удалять администраторов')


async def process_delete_admin_step(message: types.Message, state: FSMContext):
    for user_key, user_value in USERS.items():
        if user_value.nickname == message.text:
            user_value.is_admin = False
            await message.answer('Администратор удален!')
            await bot.send_message(user_key, 'Ты удален из администраторов!')
            await state.finish()
            return
    await message.answer('Человека с таким никнеймом нет в чате. Повтори попытку')


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(register_admin, commands='register_admin', state='*')
    dp.register_message_handler(process_add_admin_step, state=AdminState.add)
    dp.register_message_handler(delete_admin, commands='delete_admin', state='*')
    dp.register_message_handler(process_delete_admin_step, state=AdminState.delete)