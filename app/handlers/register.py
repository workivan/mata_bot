from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import app.config
from app.user import User


class Register(StatesGroup):
    password = State()
    nickname = State()


async def register(message: types.Message):
    if message.chat.id in app.config.USERS:
        await message.reply('Вы уже зарегистрированы!')
    else:
        await message.reply('Введите пароль для продолжения регистрации')
        await Register.password.set()


async def process_password_step(message: types.Message, state: FSMContext):
    if app.config.PASSWORD == message.text:
        await Register.next()
        await message.reply("Верный пароль. Теперь введите никнейм!")
    else:
        await message.reply('Пароль не тот, Вы не можете войти в чат! Начните регистрацию заново')
        await state.finish()


async def process_nickname_step(message: types.Message, state: FSMContext):
    for user_key, user_value in await app.config.USERS.items():
        if user_value.nickname == message.text:
            await message.reply("Этот никнейм уже занят. Введите другой!")
            return
    user_id = message.chat.id
    nickname = message.text
    username = message.chat.username
    await app.config.USERS.update({user_id: User(nickname, username, True)})
    await message.reply('''Никнейм свободен! Вы зарегистрированы и можете начать общение.\n'''
                        '''Пожалуйста, сначала ознакомьтесь с Правилами чата (это очень важно):'''
                        '''В чате запрещено:
1. Ссылки в любом виде
2. Картинки, фото, GIF, видео, стикеры
3. Голосовые сообщения 
4. Призыв к противоправным действиям
5. Непристойное общение (мат, оскорбления)
6. Флуд (написание более трех сообщений подряд в короткий промежуток времени)
7. Спам в любом его проявлении
8. Приглашать друзей без регистрации их у @fv_sergey
9. Список может пополниться (мы уведомим Вас)

Чат абсолютно анонимный (ни у кого нет возможности увидеть Ваш профиль, личные данные, кроме Администраторов чата).
 Для сохранения полной анонимности советуем не присылать в чат личные данные (никнейм профиля, номер телефона, паспортные и иные данные).

Актуальный пароль чата Вы всегда можете узнать здесь:
ссылка на группу телеграм или уточните у @fv_sergey

Чем может быть полезен чат?
- Знакомства и оффтоп общение
- Уточнение обстановки в заведении
- Поиск компании для времяпровождения и игр (PlayStation/МАФИЯ/ИНОЕ)
- Помощь в поиске чего-то / кого-то
- Обмен мнениями, опытом и многое другое

Команды в помощь:
/pin_message - увидеть закрепленное сообщение
/pause_chat - прекратить получние сообщений
/go_chat - возобновить получение сообщений'''
                        '''Приятного общения :) Напиши что-нибудь сейчас ;)''')
    await state.finish()


def register_handlers_register(dp: Dispatcher):
    dp.register_message_handler(register, commands=['register'], state="*")
    dp.register_message_handler(process_password_step, state=Register.password)
    dp.register_message_handler(process_nickname_step, state=Register.nickname)
