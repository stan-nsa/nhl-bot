from aiogram import types, Dispatcher
from nhl import nhl


async def command_standings(message: types.Message):
    await message.answer(f"<b>Турнирная таблица:</b>\n{nhl.get_standings_text(full=False)}", parse_mode="HTML")


def register_handlers_nhl(dp : Dispatcher):
    dp.register_message_handler(command_standings, commands=['standings'])
