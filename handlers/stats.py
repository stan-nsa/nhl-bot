from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from nhl import nhl, stats
from nhl import keyboards


async def command_stats(message: types.Message):
    #await message.answer(f"<b>Статистика:</b>\n{stats.get_stats_text(full=False)}", parse_mode="HTML")
    await command_stats_skaters(message)
    await command_stats_goalies(message)
    await command_stats_defensemen(message)
    await command_stats_rookies(message)



async def command_stats_skaters(message: types.Message):
    await message.answer(f"<b>Статистика игроков:</b>\n{stats.get_stats_skaters_byProperty_text(property='points', full=False)}", parse_mode="HTML",
                         reply_markup=keyboards.keyboard_stats_skaters())


async def command_stats_goalies(message: types.Message):
    await message.answer(f"<b>Статистика вратарей:</b>\n{stats.get_stats_goalies_byProperty_text(property='goalsAgainstAverage', direction='ASC', full=False)}", parse_mode="HTML",
                         reply_markup=keyboards.keyboard_stats_goalies())


async def command_stats_defensemen(message: types.Message):
    await message.answer(f"<b>Статистика защитников:</b>\n{stats.get_stats_defensemen_byProperty_text(property='points', full=False)}", parse_mode="HTML",
                         reply_markup=keyboards.keyboard_stats_defensemen())


async def command_stats_rookies(message: types.Message):
    await message.answer(f"<b>Статистика новичков:</b>\n{stats.get_stats_rookies_byProperty_text(property='points', full=False)}", parse_mode="HTML",
                         reply_markup=keyboards.keyboard_stats_rookies())


async def command_stats_skaters_kb(callback : types.CallbackQuery):
    stata = callback.data.split('_')[2]
    await callback.message.answer(
        f"<b>Статистика игроков:</b>\n{stats.get_stats_skaters_byProperty_text(property=stata, full=False)}", parse_mode="HTML",
        reply_markup=keyboards.keyboard_stats_skaters())
    await callback.answer()


async def command_stats_goalies_kb(callback : types.CallbackQuery):
    stata = callback.data.split('_')[2]
    await callback.message.answer(
        f"<b>Статистика вратарей:</b>\n{stats.get_stats_goalies_byProperty_text(property=stata, full=False)}", parse_mode="HTML",
        reply_markup=keyboards.keyboard_stats_goalies())
    await callback.answer()


async def command_stats_defensemen_kb(callback : types.CallbackQuery):
    stata = callback.data.split('_')[2]
    await callback.message.answer(
        f"<b>Статистика защитников:</b>\n{stats.get_stats_defensemen_byProperty_text(property=stata, full=False)}", parse_mode="HTML",
        reply_markup=keyboards.keyboard_stats_defensemen())
    await callback.answer()


async def command_stats_rookies_kb(callback : types.CallbackQuery):
    stata = callback.data.split('_')[2]
    await callback.message.answer(
        f"<b>Статистика новичков:</b>\n{stats.get_stats_rookies_byProperty_text(property=stata, full=False)}", parse_mode="HTML",
        reply_markup=keyboards.keyboard_stats_rookies())
    await callback.answer()


def register_handlers_stats(dp : Dispatcher):
    dp.register_message_handler(command_stats, commands=['stats'])
    dp.register_message_handler(command_stats_skaters, commands=['stats_skaters'])
    dp.register_message_handler(command_stats_goalies, commands=['stats_goalies'])
    dp.register_message_handler(command_stats_defensemen, commands=['stats_defensemen'])
    dp.register_message_handler(command_stats_rookies, commands=['stats_rookies'])
    dp.register_callback_query_handler(command_stats_skaters_kb, Text(startswith='stats_skaters_'))
    dp.register_callback_query_handler(command_stats_goalies_kb, Text(startswith='stats_goalies_'))
    dp.register_callback_query_handler(command_stats_defensemen_kb, Text(startswith='stats_defensemen_'))
    dp.register_callback_query_handler(command_stats_rookies_kb, Text(startswith='stats_rookies_'))

