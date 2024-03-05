from aiogram import Bot
from aiogram.dispatcher import Dispatcher

#-- Чтение конфига --
import json
with open('config.json') as f:
    config = json.load(f)
#----

api_token_key = 'API_TOKEN'
#api_token_key = 'API_TOKEN_TEST'

bot = Bot(token=config[api_token_key])

dp = Dispatcher(bot)

