from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from nhl import schedule
from nhl import keyboards
from nhl import nhl


async def command_scores(message: types.Message):
    data = schedule.get_scores()
    day = schedule.get_correct_date_from_data(data)

    await message.answer(
        f"{nhl.ico['scores']} <b>Scores:</b>\n{schedule.get_scores_text(data, hideScore=nhl.hide_score)}",
        parse_mode="HTML",
        reply_markup=keyboards.keyboard_scores(day))


async def command_schedule_details_day(callback: types.CallbackQuery):
    callback_data_parts = callback.data.split('_')
    day = callback_data_parts[3]

    games = schedule.get_schedule_day_games_for_inlinemenu(day)

    if (callback_data_parts[0] == 'Scores'):
        await callback.message.edit_text(
            f"{nhl.ico['scores']} <b>Scores:</b>\n{day}",
            parse_mode="HTML",
            reply_markup=keyboards.keyboard_schedule_details(games))
    else:
        await callback.message.answer(
            f"{nhl.ico['scores']} <b>Scores:</b>\n{day}",
            parse_mode="HTML",
            reply_markup=keyboards.keyboard_schedule_details(games))

    await callback.answer()


async def command_schedule(message: types.Message):
    dates = schedule.get_schedule_dates_for_inlinemenu()
    await message.answer(
        f"{nhl.ico['schedule']} <b>Schedule:</b>\n{schedule.get_schedule_day_text(hideScore=nhl.hide_score)}",
        parse_mode="HTML",
        reply_markup=keyboards.keyboard_schedule(dates))


async def command_schedule_day(callback: types.CallbackQuery):
    callback_data_parts = callback.data.split('_')
    day = callback_data_parts[2]

    dates = schedule.get_schedule_dates_for_inlinemenu(day)

    #await callback.message.answer(
    await callback.message.edit_text(
        f"{nhl.ico['schedule']} <b>Schedule:</b>\n{schedule.get_schedule_day_text(day=day, hideScore=nhl.hide_score)}",
        parse_mode="HTML",
        reply_markup=keyboards.keyboard_schedule(dates))

    await callback.answer()


async def command_gameday(message: types.Message):
    await message.answer(f"#GameDay - {schedule.get_schedule_day_text()}", parse_mode="HTML")


async def command_schedule_team(message: types.Message):
    await message.answer(
        f"{nhl.ico['schedule']} <b>Расписание матчей любимых команд:</b>\n{schedule.get_schedule_user_teams(message.from_user)}",
        parse_mode="HTML")


def register_handlers_schedule(dp: Dispatcher):
    dp.register_message_handler(command_scores, commands=['scores'])
    dp.register_message_handler(command_schedule, commands=['schedule'])
    dp.register_message_handler(command_gameday, commands=['gameday'])
    dp.register_callback_query_handler(command_schedule_day, Text(startswith='Schedule_day'))
    dp.register_callback_query_handler(command_schedule_details_day, Text(startswith='Schedule_Details_day'))
    dp.register_callback_query_handler(command_schedule_details_day, Text(startswith='Scores_Details_day'))
