from aiogram import Dispatcher, types


def test(message: types.Message):
    print('test')


def register_handlers_test(dp: Dispatcher):
    dp.register_message_handler(test, commands='test', state='*')