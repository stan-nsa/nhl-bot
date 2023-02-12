from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from emoji import emojize #Overview of all emoji: https://carpedm20.github.io/emoji/

from nhl import schedule
from nhl import keyboards


async def command_scores(message: types.Message):
    await message.answer(f"{emojize(':goal_net::ice_hockey:')} <b>Scores:</b>\n{schedule.get_scores_text()}", parse_mode="HTML",
                         reply_markup=keyboards.keyboard_scores())


async def command_scores_details(callback : types.CallbackQuery):
    await callback.message.answer(f"{emojize(':goal_net::ice_hockey:')} <b>Scores:</b>\n{schedule.get_scores_text(details=True)}", parse_mode="HTML",
                                  reply_markup=keyboards.keyboard_scores_details())
    await callback.answer()


async def command_scores_games_details(callback : types.CallbackQuery):
    data = schedule.get_scores()

    for date_day in data['dates']:

        await callback.message.answer(f"{emojize(':goal_net::ice_hockey:')} <b>Scores:</b>\n", parse_mode="HTML")

        for game in date_day['games']:
            await callback.message.answer(f"{schedule.get_schedule_day_game_text(game, withHeader=True)}", parse_mode="HTML",
                                          reply_markup=keyboards.keyboard_scores_game_details(game))
    await callback.answer()


async def command_scores_game_details(callback : types.CallbackQuery):
    callback_data_parts = callback.data.split('_')
    game_id = callback_data_parts[4]

    await callback.answer(f"Game ID: {game_id}", show_alert=True)

    await callback.answer()


async def command_schedule(message: types.Message):
    dates = schedule.get_schedule_dates_for_inlinemenu()
    await message.answer(f"{emojize(':calendar:')} <b>Schedule:</b>\n{schedule.get_schedule_day_text()}", parse_mode="HTML",
                         reply_markup=keyboards.keyboard_schedule(dates))


async def command_schedule_day(callback : types.CallbackQuery):
    callback_data_parts = callback.data.split('_')
    day = callback_data_parts[2]

    # если в callback.data присутствует '_details', то дополнительно выводится scoring-информация
    details = True if (len(callback_data_parts) > 3) else False

    dates = schedule.get_schedule_dates_for_inlinemenu(day)
    await callback.message.answer(f"{emojize(':calendar:')} <b>Schedule:</b>\n{schedule.get_schedule_day_text(day, details=details)}", parse_mode="HTML",
                                  reply_markup=keyboards.keyboard_schedule(dates))
    await callback.answer()


async def command_gameday(message: types.Message):
    await message.answer(f"#GameDay - {schedule.get_schedule_day_text()}", parse_mode="HTML")


async def command_schedule_team(message: types.Message):
    await message.answer(f"{emojize(':calendar:')} <b>Расписание матчей любимых команд:</b>\n{schedule.get_schedule_user_teams(message.from_user)}", parse_mode="HTML")


def register_handlers_schedule(dp: Dispatcher):
    dp.register_message_handler(command_scores, commands=['scores'])
    dp.register_message_handler(command_schedule, commands=['schedule'])
    dp.register_message_handler(command_gameday, commands=['gameday'])
    dp.register_callback_query_handler(command_scores_details, Text('schedule_scores_details'))
    dp.register_callback_query_handler(command_scores_games_details, Text('schedule_scores_games_details'))
    dp.register_callback_query_handler(command_scores_game_details, Text(startswith='schedule_scores_game_details'))
    dp.register_callback_query_handler(command_schedule_day, Text(startswith='schedule_day_'))
