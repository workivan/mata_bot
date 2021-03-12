from aiogram import Dispatcher, types
from app.config import *


async def start_message(message: types.Message):
    await message.reply(
        'Привет. Я твой бот для анонимного общения. \n'
        'Введи /register, чтобы зарегистрироваться \n'
        'Правила: \n',
    )


async def pin_message_send(message: types.Message):
    await message.reply(text=PIN_MESSAGE)


async def send_message(message: types.Message):
    if not USERS.get(message.chat.id).banned:
        for user_key, user_value in USERS.items():
            if user_key != message.chat.id and user_value.subscription == True:
                if not user_value.banned:
                    msg = str(user_value.nickname) + '\n' + message.text
                    await bot.send_message(user_key, text=msg)
    else:
        await message.reply('Ты в бане!')


async def send_file_error(message: types.Message):
    if message.chat.id == SUPER_USER_ID:
        for user_key, user_value in USERS.items():
            if user_key != message.chat.id and user_value.subscription == True:
                await bot.send_message(user_key, message.text)
    else:
        await message.reply('Прости, но по правилам ты можешь отправлять только текстовые сообщения '
                            'не чаще, чем раз в 30 секунд')
        await bot.delete_message(message.chat.id, message.message_id)


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(start_message, commands=['start', 'help'])
    dp.register_message_handler(pin_message_send, commands='pin_message')
    dp.register_message_handler(send_message, content_types='text')
    dp.register_message_handler(send_file_error, content_types=["sticker", "pinned_message", "photo", "audio",
                                                                "document", "video", "video_note", "voice", "location",
                                                                "contact"])