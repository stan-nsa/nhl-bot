from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from nhl import schedule
from nhl import keyboards
from nhl import nhl


async def command_scores(message: types.Message):
    data = schedule.get_scores()
    day = data['currentDate']
    txt = f"{nhl.ico['scores']} <b>Scores:</b>\n{schedule.get_scores_text(data, hideScore=nhl.hide_score)}"

    await message.answer(txt, parse_mode="HTML", reply_markup=keyboards.keyboard_scores(day))


async def command_schedule_details_day(callback: types.CallbackQuery):
    callback_data_parts = callback.data.split('_')
    day = callback_data_parts[3]
    txt = f"{nhl.ico['scores']} <b>Scores:</b>\n{day}"
    games = schedule.get_schedule_day_games_for_inlinemenu(day)
    func = callback.message.edit_text if (callback_data_parts[0] == 'Scores') else callback.message.answer

    await func(txt, parse_mode="HTML", reply_markup=keyboards.keyboard_schedule_details(games))
    await callback.answer()


async def command_schedule(message: types.Message):
    dates = schedule.get_schedule_dates_for_inlinemenu()
    txt = f"{nhl.ico['schedule']} <b>Schedule:</b>\n{schedule.get_schedule_day_text(hideScore=nhl.hide_score)}"
    await message.answer(txt, parse_mode="HTML", reply_markup=keyboards.keyboard_schedule(dates))


async def command_schedule_day(callback: types.CallbackQuery):
    day = callback.data.split('_')[2]
    dates = schedule.get_schedule_dates_for_inlinemenu(day)
    txt = f"{nhl.ico['schedule']} <b>Schedule:</b>\n{schedule.get_schedule_day_text(day=day, hideScore=nhl.hide_score)}"

    await callback.message.edit_text(txt, parse_mode="HTML", reply_markup=keyboards.keyboard_schedule(dates))
    await callback.answer()


async def command_gameday(message: types.Message):
    txt = f"#GameDay - {schedule.get_schedule_day_text()}"
    await message.answer(txt, parse_mode="HTML")


async def command_schedule_team(message: types.Message):
    txt = f"{nhl.ico['schedule']} <b>Расписание матчей любимых команд:</b>\n{schedule.get_schedule_user_teams(message.from_user)}"
    await message.answer(txt, parse_mode="HTML")


def register_handlers_schedule(dp: Dispatcher):
    dp.register_message_handler(command_scores, commands=['scores'])
    dp.register_message_handler(command_schedule, commands=['schedule'])
    dp.register_message_handler(command_gameday, commands=['gameday'])
    dp.register_callback_query_handler(command_schedule_day, Text(startswith='Schedule_day'))
    dp.register_callback_query_handler(command_schedule_details_day, Text(startswith='Schedule_Details_day'))
    dp.register_callback_query_handler(command_schedule_details_day, Text(startswith='Scores_Details_day'))
