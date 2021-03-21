from aiogram import Dispatcher, types
import app.config
from random import sample
import re

regex = r"(?P<domain>\w+\.\w{2,3})"


async def start_message(message: types.Message):
    await message.answer(
        'Привет. Я Ваш бот для анонимного общения. \n'
        'Введите /register, чтобы зарегистрироваться \n'
    )


async def pin_message_send(message: types.Message):
    await message.answer(text=app.config.PIN_MESSAGE)


async def send_message(message: types.Message):
    tmp_user = await app.config.USERS[message.chat.id]
    if message.chat.id in app.config.USERS and not tmp_user.banned and \
            tmp_user.improved and tmp_user.subscription:
        for user_key, user_value in await app.config.USERS.items():
            if user_key != message.chat.id and user_value.subscription is True:
                if not user_value.banned:
                    if re.search(regex, str(message.text)):
                        await message.answer('Вы присслали ссылку. Это запрещено.')
                        await app.config.bot.delete_message(message.chat.id, message.message_id)
                        return
                    clear_msg = []
                    for word in str(message.text).lower().split():
                        clear_msg.append(''.join(sample(app.config.FIL, len(word)))) if word in app.config.FILTER_LIST \
                            else clear_msg.append(word)
                    tmp_user = await app.config.USERS.get(message.chat.id)
                    msg = '[' + str(tmp_user.nickname) + ']: ' + ' '.join(clear_msg)
                    await app.config.bot.send_message(user_key, text=msg)
    else:
        await message.answer('Вы не можете писать!')


async def send_file_error(message: types.Message):
    for user_key, user_value in await app.config.USERS.items():
        if user_key == message.chat.id and user_value.is_admin is True:
            for key, value in await app.config.USERS.items():
                if key != message.chat.id and value.subscription is True:
                    if "photo" in message:
                        await app.config.bot.send_photo(key, str(message.photo[0].file_id))
            return
    else:
        await message.answer('Простите, но по правилам Вы можете отправлять только текстовые сообщения')
        await app.config.bot.delete_message(message.chat.id, message.message_id)


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(start_message, commands=['start', 'help'], state='*')
    dp.register_message_handler(pin_message_send, commands='pin_message', state='*')
    dp.register_message_handler(send_message, content_types='text', state='*')
    dp.register_message_handler(send_file_error, content_types=["sticker", "pinned_message", "audio",
                                                                "document", "video", "photo", "video_note", "voice",
                                                                "location", "contact"], state='*')
