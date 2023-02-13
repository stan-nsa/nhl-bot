from aiogram import Bot, Dispatcher, executor, types
from create_bot import dp
from handlers import nhl, other, schedule, stats, game


nhl.register_handlers_nhl(dp)
other.register_handlers_other(dp)
schedule.register_handlers_schedule(dp)
stats.register_handlers_stats(dp)
game.register_handlers_game(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
