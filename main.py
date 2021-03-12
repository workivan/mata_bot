import telebot
from user import User
from config import TOKEN, SUPER_USER_ID, SUPER_USER_LOGIN, SUPER_USER_NICKNAME

bot = telebot.TeleBot(TOKEN)

users = dict()

super_user = User(SUPER_USER_NICKNAME, SUPER_USER_LOGIN, True, False, True, True)
users.update({SUPER_USER_ID: super_user})


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
                     'Привет. Я бот. Вот правила:')


# @bot.message_handler(commands=['admin'])
# def console_admin(message):
#     pass


@bot.message_handler(commands='delete_user')
def delete_user(message):
    if message.chat.id in users:
        msg = bot.send_message(message.chat.id, 'Введи никнейм того, кого хочешь удалить')
        bot.register_next_step_handler(msg, process_delete_user_step)


@bot.message_handler(commands=['register_admin'])
def register_admin(message):
    if int(message.chat.id) == SUPER_USER_ID:
        msg = bot.reply_to(message, "Введи никнейм того, кого хочешь сделать админстратором")
        bot.register_next_step_handler(msg, process_add_admin_step)


@bot.message_handler(commands=['delete_admin'])
def delete_admin(message):
    if int(message.chat.id) == SUPER_USER_ID:
        msg = bot.reply_to(message, "Введи никнейм того, кого хочешь удалить из админстратором")
        bot.register_next_step_handler(msg, process_delete_admin_step)


@bot.message_handler(commands=['register'])
def register(message):
    if message.chat.id in users:
        bot.send_message(message.chat.id, 'Ты уже зарегистрирован!')
    else:
        msg = bot.reply_to(message, "Введи свой никнейм")
        bot.register_next_step_handler(msg, process_nickname_step)


def process_add_admin_step(message):
    for user_key, user_value in users.items():
        if user_value.nickname == message.text:
            user_value.is_admin = True
            bot.send_message(message.chat.id, 'Новый администратор добавлен')
            bot.send_message(user_key, 'Теперь ты администратор')


def process_delete_user_step(message):
    for user_key, user_value in users.items():
        if user_value.nickname == message.text:
            user_value.banned = True
            bot.send_message(message.chat.id, 'Пользователь удален')
            bot.send_message(user_key, 'Ты забанен в чате')


def process_delete_admin_step(message):
    for user_key, user_value in users.items():
        if user_value.nickname == message.text:
            user_value.is_admin = False
            bot.send_message(message.chat.id, 'Администратор удален')
            bot.send_message(user_key, 'Ты удален из администраторов')


def process_nickname_step(message):
    user_id = message.chat.id
    nickname = message.text
    username = message.chat.username
    users.update({user_id: User(nickname, username)})


@bot.message_handler(content_types=['text'])
def send_message(message):
    for user_key, user_value in users.items():
        if user_key != message.chat.id and user_value.subscription is True:
            bot.send_message(user_key, message.text)


@bot.message_handler(content_types=["sticker", "pinned_message", "photo", "audio", "document", "video", "video_note", "voice", "location", "contact"])
def send_image_error(message):
    bot.send_message(message.chat.id, 'Прости, но по правилам ты можешь отправлять только текстовые сообщения не чаще,'
                                      'чем раз в минуту')
    bot.delete_message(message.chat.id, message.message_id)


if __name__ == '__main__':
    bot.infinity_polling()
