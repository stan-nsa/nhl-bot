from aiogram import Bot
from aiogram.dispatcher import Dispatcher

#-- Чтение конфига --
import json
with open('config.json') as f:
    config = json.load(f)
#----


bot = Bot(token=config['API_TOKEN'])
dp = Dispatcher(bot)

