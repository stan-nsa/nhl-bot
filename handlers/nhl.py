from aiogram import types, Dispatcher, exceptions
from nhl import nhl
from nhl import keyboards

from aiogram.dispatcher.filters import Text


async def command_standings(message: types.Message):
    txt = f"{nhl.ico['standings']}<b>Standings:</b>\n{nhl.get_standings_text(full=True)}"
    await message.answer(txt, parse_mode="HTML", reply_markup=keyboards.keyboard_standings())


async def command_standings_type(callback: types.CallbackQuery):
    standings_type = callback.data.split('_')[1]

    txt = f"{nhl.ico['standings']}<b>Standings:</b>\n{nhl.get_standings_text(standings_type, full=True)}"

    try:
        await callback.message.edit_text(txt, parse_mode="HTML", reply_markup=keyboards.keyboard_standings())

    except exceptions.MessageNotModified:
        pass

    finally:
        await callback.answer()


async def command_teams(message: types.Message):
    teams = nhl.get_teams()
    txt = f"{nhl.ico['hockey']}<b>Teams:</b>"
    await message.answer(txt, parse_mode="HTML", reply_markup=keyboards.keyboard_teams(teams))


async def command_team_info(callback: types.CallbackQuery):
    teamAbbrev_teamName, info = callback.data.split('_')[1:]

    # Функция для ответа
    if info == 'button':
        func = callback.message.answer
        info = 'info'
    else:
        func = callback.message.edit_text

    txt = f"{nhl.ico['hockey']}<b>Team:</b>\n{nhl.get_team_info(teamAbbrev_teamName, info=info)}"

    try:
        await func(txt, parse_mode="HTML", reply_markup=keyboards.keyboard_team(teamAbbrev_teamName))

    except exceptions.MessageNotModified:
        pass

    finally:
        await callback.answer()


def register_handlers_nhl(dp: Dispatcher):
    dp.register_message_handler(command_standings, commands=['standings'])
    dp.register_message_handler(command_teams, commands=['teams'])
    dp.register_callback_query_handler(command_standings_type, Text(startswith='standings_'))
    dp.register_callback_query_handler(command_team_info, Text(startswith='team_'))

