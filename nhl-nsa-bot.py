from aiogram import Bot, Dispatcher, executor, types
from create_bot import dp
from handlers import other, schedule, stats

other.register_handlers_other(dp)
schedule.register_handlers_schedule(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
