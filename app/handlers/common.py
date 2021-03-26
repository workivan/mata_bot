from aiogram import Dispatcher, types
import app.config
import re


async def start_message(message: types.Message):
    await message.answer(
        'Привет. Я Ваш бот для анонимного общения. \n'
        'Введите /register, чтобы зарегистрироваться \n'
    )


async def pin_message_send(message: types.Message):
    await message.answer(text=app.config.PIN_MESSAGE)


async def send_message(message: types.Message):
    user = await app.config.USERS[message.chat.id]
    if message.chat.id in app.config.USERS and not user.banned and user.subscription:
        for user_key, user_value in await app.config.USERS.items():
            if user_key != message.chat.id and user_value.subscription and not user_value.banned:
                if re.search(app.config.REGEX, str(message.text)):
                    await message.answer('Вы присслали ссылку. Это запрещено.')
                    await app.config.bot.delete_message(message.chat.id, message.message_id)
                    return
                for word in app.config.FILTER_LIST:
                    if re.search(word, str.lower(message.text)):
                        await message.answer('Вы ругаетесь. Это запрещено.')
                        await app.config.bot.delete_message(message.chat.id, message.message_id)
                        return
                msg = '[ ' + str(user.nickname) + ' ]: ' + ''.join(message.text)
                await app.config.bot.send_message(user_key, text=msg)
    else:
        await message.answer('Вы не можете писать!')


async def send_file_error(message: types.Message):
    for user_key, user_value in await app.config.USERS.items():
        if user_key == message.chat.id and user_value.is_admin:
            for key, value in await app.config.USERS.items():
                if key != message.chat.id and value.subscription:
                    if "photo" in message:
                        await app.config.bot.send_photo(key, str(message.photo[0].file_id))
            return
    else:
        await message.answer('Простите, но по правилам Вы можете отправлять только текстовые сообщения')
        await app.config.bot.delete_message(message.chat.id, message.message_id)


async def get_online_users(message: types.Message):
    users_online = []
    for key, value in await app.config.USERS.items():
        if value.subscription and key != message.chat.id:
            users_online.append(f"- {value.nickname}\n")
    if users_online:
        await message.answer(f"Сейчас в чате: ")
        await message.answer(text="".join(users_online))
    else:
        await message.answer("Никого в чате нет")


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(start_message, commands=['start', 'help'], state='*')
    dp.register_message_handler(pin_message_send, commands='pin_message', state='*')
    dp.register_message_handler(get_online_users, commands='in_chat', state='*')
    dp.register_message_handler(send_message, content_types='text', state='*')
    dp.register_message_handler(send_file_error, content_types=["sticker", "pinned_message", "audio",
                                                                "document", "video", "photo", "video_note", "voice",
                                                                "location", "contact"], state='*')
