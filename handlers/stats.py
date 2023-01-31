from aiogram import types, Dispatcher
from nhl import nhl, stats


async def command_stats(message: types.Message):
    await message.answer(f"<b>Статистика:</b>\n{stats.get_stats_text(full=False)}", parse_mode="HTML")


async def command_stats_goalie(message: types.Message):
    await message.answer(f"<b>Статистика вратарей:</b>\n{stats.get_stats_goalie_text(full=False)}", parse_mode="HTML")

async def command_stats_skater(message: types.Message):
    await message.answer(f"<b>Статистика игроков:</b>\n{stats.get_stats_skater_text(full=False)}", parse_mode="HTML")


def register_handlers_stats(dp : Dispatcher):
    dp.register_message_handler(command_stats, commands=['stats'])
    dp.register_message_handler(command_stats_goalie, commands=['stats_goalie'])
    dp.register_message_handler(command_stats_skater, commands=['stats_skater'])
