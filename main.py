import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from user import User
from config import *

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

logger = logging.getLogger(__name__)

users = dict()
super_user = User(SUPER_USER_NICKNAME, SUPER_USER_LOGIN, True, False, True, True)
users.update({SUPER_USER_ID: super_user})


class Register(StatesGroup):
    password = State()
    nickname = State()


class AdminState(StatesGroup):
    add = State()
    delete = State()


class UserState(StatesGroup):
    delete = State()


@dp.message_handler(commands=['start', 'help'])
async def start_message(message: types.Message):
    await message.reply(
        'Привет. Я твой бот для анонимного общения. \n'
        'Введи /register, чтобы зарегистрироваться \n'
        'Правила: \n'
    )


@dp.message_handler(commands='delete_user')
async def delete_user(message: types.Message):
    for user_key, user_value in users.items():
        if user_key == message.chat.id and user_value.is_admin == True:
            await message.reply('Введи никнейм того, кого хочешь удалить')
            await UserState.delete.set()
        else:
            await message.reply('Ты не можешь банить пользователей')


@dp.message_handler(state=UserState.delete)
async def process_delete_user_step(message: types.Message, state: FSMContext):
    for user_key, user_value in users.items():
        if user_value.nickname == message.text:
            user_value.banned = True
            await message.answer('Пользователь удален!')
            await bot.send_message(user_key, 'Ты забанен в чате!')
            await state.finish()
            return
    await message.answer('Человека с таким никнеймом нет в чате')


@dp.message_handler(commands=['register_admin'])
async def register_admin(message: types.Message):
    if int(message.chat.id) == SUPER_USER_ID:
        await message.reply('Введи никнейм того, кого хочешь сделать администратором')
        await AdminState.add.set()
    else:
        await bot.send_message(message.chat.id, 'Ты не можешь добавлять новых администраторов')


@dp.message_handler(state=AdminState.add)
async def process_add_admin_step(message: types.Message, state: FSMContext):
    for user_key, user_value in users.items():
        if user_value.nickname == message.text:
            user_value.is_admin = True
            await message.answer('Новый администратор добавлен!')
            await bot.send_message(user_key, 'Теперь ты администратор!')
            await state.finish()
            return
    await message.answer('Человека с таким никнеймом нет в чате')


@dp.message_handler(commands=['delete_admin'])
async def delete_admin(message: types.Message):
    if int(message.chat.id) == SUPER_USER_ID:
        await message.reply('Введи никнейм того, кого хочешь удалить из админстратором')
        await AdminState.delete.set()
    else:
        await bot.send_message(message.chat.id, 'Ты не можешь удалять администраторов')


@dp.message_handler(state=AdminState.delete)
async def process_delete_admin_step(message: types.Message, state: FSMContext):
    for user_key, user_value in users.items():
        if user_value.nickname == message.text:
            user_value.is_admin = False
            await message.answer('Администратор удален!')
            await bot.send_message(user_key, 'Ты удален из администраторов!')
            await state.finish()
            return
    await message.answer('Человека с таким никнеймом нет в чате')


@dp.message_handler(commands=['register'])
async def register(message: types.Message):
    if message.chat.id in users:
        await message.reply('Ты уже зарегистрирован!')
    else:
        await message.reply('Введи пароль для продолжения регистрации')
        await Register.password.set()


@dp.message_handler(state=Register.password)
async def process_password_step(message: types.Message):
    if PASSWORD == message.text:
        await Register.next()
        await message.reply("Верный пороль. Теперь введи никнейм!")
    else:
        await message.reply('Пороль не тот, ты не можешь войти в чат!')


@dp.message_handler(state=Register.nickname)
async def process_nickname_step(message: types.Message, state: FSMContext):
    for user_key, user_value in users.items():
        if user_value.nickname == message.text:
            await message.reply("Этот никнейм уже занят. Выбери другой!")
            return
    user_id = message.chat.id
    nickname = message.text
    username = message.chat.username
    users.update({user_id: User(nickname, username)})
    await message.reply("Никнейм свободен. Можешь начать общение!")
    await state.finish()


@dp.message_handler(content_types=['text'])
async def send_message(message: types.Message):
    if not users.get(message.chat.id).banned:
        for user_key, user_value in users.items():
            if user_key != message.chat.id and user_value.subscription == True:
                if not user_value.banned:
                    await bot.send_message(user_key, message.text)
    else:
        await message.reply('Ты в бане!')


@dp.message_handler(content_types=["sticker", "pinned_message", "photo", "audio", "document", "video", "video_note",
                                   "voice", "location", "contact"])
async def send_image_error(message: types.Message):
    if message.chat.id == SUPER_USER_ID:
        for user_key, user_value in users.items():
            if user_key != message.chat.id and user_value.subscription == True:
                await bot.send_message(user_key, message.text)
    else:
        await message.reply('Прости, но по правилам ты можешь отправлять только текстовые сообщения '
                            'не чаще, чем раз в 30 секунд')
        await bot.delete_message(message.chat.id, message.message_id)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.info("Starting bot")

    try:
        await dp.start_polling()
    finally:
        await bot.close()

if __name__ == '__main__':
    asyncio.run(main())
