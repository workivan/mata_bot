from aiogram import Dispatcher, types
import app.config
from random import sample
import re

regex = r"(?P<domain>\w+\.\w{2,3})"


async def start_message(message: types.Message):
    await message.answer(
        'Привет. Я твой бот для анонимного общения. \n'
        'Введи /register, чтобы зарегистрироваться \n'
        'Правила: \n',
    )


async def pin_message_send(message: types.Message):
    await message.answer(text=app.config.PIN_MESSAGE)


async def send_message(message: types.Message):
    if message.chat.id in app.config.USERS and not app.config.USERS.get(message.chat.id).banned and \
            app.config.USERS.get(message.chat.id).improved and app.config.USERS.get(message.chat.id).subscription:
        for user_key, user_value in app.config.USERS.items():
            if user_key != message.chat.id and user_value.subscription == True:
                if not user_value.banned:
                    if re.search(regex, str(message.text)):
                        await message.answer('Ты скинул ссылку. Это запрещено.')
                        await app.config.bot.delete_message(message.chat.id, message.message_id)
                        return
                    clear_msg = []
                    for word in str(message.text).lower().split():
                        clear_msg.append(''.join(sample(app.config.FIL, len(word)))) if word in app.config.FILTER_LIST \
                            else clear_msg.append(word)
                    msg = '[' + str(app.config.USERS.get(message.chat.id).nickname) + ']: ' + ' '.join(clear_msg)
                    await app.config.bot.send_message(user_key, text=msg)
    else:
        await message.answer('Ты не можешь писать!')


async def send_file_error(message: types.Message):
    for user_key, user_value in app.config.USERS.items():
        if user_key == message.chat.id and user_value.is_admin == True:
            for user_key_1, user_value_1 in app.config.USERS.items():
                if user_key_1 != message.chat.id and user_value_1.subscription == True:
                    if "photo" in message:
                        await app.config.bot.send_photo(user_key_1, str(message.photo[0].file_id))
                        return
        else:
            await message.answer('Прости, но по правилам ты можешь отправлять только текстовые сообщения')
            await app.config.bot.delete_message(message.chat.id, message.message_id)


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(start_message, commands=['start', 'help'], state='*')
    dp.register_message_handler(pin_message_send, commands='pin_message', state='*')
    dp.register_message_handler(send_message, content_types='text', state='*')
    dp.register_message_handler(send_file_error, content_types=["sticker", "pinned_message", "photo", "audio",
                                                                "document", "video", "video_note", "voice", "location",
                                                                "contact"], state='*')