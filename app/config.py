from aiogram import Bot

SUPER_USER_NICKNAME = 'gwenbleyd'
TOKEN = '1652503829:AAEO9y_OuSiw3bGzNMG2sehrH8HjD5DrUu0'
SUPER_USER_LOGIN = 'gwenbleyd'
PASSWORD = '841XcTNeYD'
SUPER_USER_ID = 447959709
PIN_MESSAGE = 'Это первое закрепленное сообщение для проверки'
bot = Bot(token=TOKEN)
USERS = dict()

FIL = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")"]

with open('filter.txt', 'r') as f:
    FILTER_LIST = f.read().splitlines()