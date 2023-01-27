from aiogram import Bot, Dispatcher, executor, types
from create_bot import dp


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
