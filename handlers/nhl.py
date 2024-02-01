import json

from aiogram import types, Dispatcher
from nhl import nhl
from nhl import keyboards

from aiogram.dispatcher.filters import Text


async def command_standings(message: types.Message):
    await message.answer(
        f"{nhl.ico['standings']}<b>Standings:</b>\n{nhl.get_standings_text(full=True)}",
        parse_mode="HTML",
        reply_markup=keyboards.keyboard_standings())


async def command_standings_type(callback: types.CallbackQuery):
    standings_type = callback.data.split('_')[1]
    try:
        #await callback.message.answer(
        await callback.message.edit_text(
            f"{nhl.ico['standings']}<b>Standings:</b>\n{nhl.get_standings_text(standings_type, full=True)}",
            parse_mode="HTML",
            reply_markup=keyboards.keyboard_standings())
        await callback.answer()

    except:
        await callback.answer()


async def command_teams(message: types.Message):
    teams = nhl.get_teams()
    await message.answer(
        f"{nhl.ico['standings']}<b>Teams:</b>",
        parse_mode="HTML",
        reply_markup=keyboards.keyboard_teams(teams))


async def command_team_info(callback: types.CallbackQuery):
    teamAbbrev = callback.data.split('_')[1]

    try:
        await callback.message.answer(
            f"{nhl.ico['standings']}<b>Team:</b>\n{nhl.get_team_info(teamAbbrev)}",
            parse_mode="HTML",
            reply_markup=keyboards.keyboard_team(teamAbbrev))
        await callback.answer()

    except:
        await callback.answer()


def register_handlers_nhl(dp: Dispatcher):
    dp.register_message_handler(command_standings, commands=['standings'])
    dp.register_message_handler(command_teams, commands=['teams'])
    dp.register_callback_query_handler(command_standings_type, Text(startswith='standings_'))
    dp.register_callback_query_handler(command_team_info, Text(startswith='team_'))

