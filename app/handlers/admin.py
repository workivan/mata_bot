from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from app.config import *


class AdminState(StatesGroup):
    add = State()
    delete = State()


async def register_admin(message: types.Message):
    if int(message.chat.id) == SUPER_USER_ID:
        await message.reply('Введите никнейм того, кого нужно сделать администратором')
        await AdminState.add.set()
    else:
        await message.reply('Вы не можете добавлять новых администраторов')


async def process_add_admin_step(message: types.Message, state: FSMContext):
    admin_added = False
    for user_key, user_value in await USERS.items():
        if user_value.nickname == message.text:
            user_value.is_admin = True
            await message.answer('Новый администратор добавлен!')
            await bot.send_message(user_key, 'Теперь Вы администратор!')
            await USERS.update({user_key: user_value})
            admin_added = True
    if not admin_added:
        await message.answer('Человека с таким никнеймом нет в чате.')
    await state.finish()


async def delete_admin(message: types.Message):
    if int(message.chat.id) == SUPER_USER_ID:
        await message.reply('Введите никнейм того, кого нужно удалить из админстраторов')
        await AdminState.delete.set()
    else:
        await message.reply('Вы не можете удалять администраторов')


async def process_delete_admin_step(message: types.Message, state: FSMContext):
    admin_deleted = False
    for user_key, user_value in await USERS.items():
        if user_value.nickname == message.text:
            user_value.is_admin = False
            await message.answer('Администратор удален!')
            await bot.send_message(user_key, 'Вы удалены из администраторов!')
            await USERS.update({user_key: user_value})
            admin_deleted = True
    if not admin_deleted:
        await message.answer('Человека с таким никнеймом нет в администраторах.')
    await state.finish()


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(register_admin, commands='add_admin', state='*')
    dp.register_message_handler(process_add_admin_step, state=AdminState.add)
    dp.register_message_handler(delete_admin, commands='delete_admin', state='*')
    dp.register_message_handler(process_delete_admin_step, state=AdminState.delete)
