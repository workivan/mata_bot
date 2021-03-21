from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from app.config import *


class UserState(StatesGroup):
    delete = State()
    add = State()


async def delete_user(message: types.Message):
    tmp_user = await USERS.get(message.chat.id)
    if tmp_user.is_admin:
        for user_key, user_value in await USERS.items():
            if user_key == message.chat.id:
                await message.answer('Введите никнейм того, кого нужно забанить')
                await UserState.delete.set()
                return
    else:
        await message.answer('Вы не можете банить пользователей')


async def process_delete_user_step(message: types.Message, state: FSMContext):
    is_ban = False
    for user_key, user_value in await USERS.items():
        tmp_user = await USERS.get(message.chat.id)
        if message.text != SUPER_USER_NICKNAME:
            if user_value.nickname == message.text and user_value.is_admin is False and tmp_user.is_admin is True:
                user_value.banned = True
                await USERS.update({user_key: user_value})
                await message.answer('Пользователь забанен!')
                await message.answer('Его логин в телеграм - @' + str(user_value.login))
                await bot.send_message(user_key, 'Вы забанены в чате!')
                is_ban = True
    if not is_ban:
        await message.answer('Вы не можете этого сделать')
    await state.finish()


async def add_user(message: types.Message):
    tmp_user = await USERS.get(message.chat.id)
    if tmp_user.is_admin:
        for user_key, user_value in await USERS.items():
            if user_key == message.chat.id:
                await message.answer('Введите никнейм того, кого нужно разбанить')
                await UserState.add.set()
                return
    else:
        await message.answer('Вы не можете разбанить пользователей')


async def process_add_user_step(message: types.Message, state: FSMContext):
    is_un_ban = False
    tmp_user = await USERS.get(message.chat.id)
    for user_key, user_value in await USERS.items():
        if user_value.nickname == message.text and tmp_user.is_admin is True:
            user_value.banned = False
            await USERS.update({user_key: user_value})
            await message.answer('Пользователь возвращен!')
            await bot.send_message(user_key, 'Вы разбанены в чате!')
            is_un_ban = True
    if not is_un_ban:
        await message.answer('Вы не можете этого сделать')
    await state.finish()


async def pause_mess(message: types.Message):
    if message.chat.id in USERS:
        user = await USERS.get(message.chat.id)
        if user.subscription:
            user.subscription = False
            await USERS.update({message.chat.id: user})
            await message.answer('Вы отписались от чата')
        else:
            await message.answer('Вы и так уже отписались от чата!')


async def proceed_mess(message: types.Message):
    if message.chat.id in USERS:
        user = await USERS.get(message.chat.id)
        if not user.subscription:
            user.subscription = True
            await USERS.update({message.chat.id: user})
            await message.answer('Вы вновь в чате!')
        else:
            await message.answer('Вы и так подписаны на чат')


def register_handlers_user(dp: Dispatcher):
    dp.register_message_handler(delete_user, commands='ban_user', state='*')
    dp.register_message_handler(process_delete_user_step, state=UserState.delete)
    dp.register_message_handler(add_user, commands='unban_user', state='*')
    dp.register_message_handler(pause_mess, commands='pause_chat', state='*')
    dp.register_message_handler(proceed_mess, commands='go_chat', state='*')
    dp.register_message_handler(process_add_user_step, state=UserState.add)
