from aiogram import types, Dispatcher
from emoji import emojize #Overview of all emoji: https://carpedm20.github.io/emoji/
from create_bot import dp

from nhl import schedule

async def command_scores(message: types.Message):
    await message.reply(f"{emojize(':goal_net::ice_hockey:')} <b>Результаты матчей:</b>\n{schedule.get_scores_text()}", parse_mode="HTML")


async def command_schedule(message: types.Message):
    await message.reply(f"{emojize(':calendar:')} <b>Расписание матчей:</b>\n{schedule.get_schedule_today_text()}", parse_mode="HTML")


async def command_schedule_today(message: types.Message):
    await message.reply(f"{emojize(':calendar:')} <b>Расписание матчей:</b>\n{schedule.get_schedule_today_text()}", parse_mode="HTML")


async def command_schedule_tomorrow(message: types.Message):
    await message.reply(f"{emojize(':calendar:')} <b>Расписание матчей:</b>\n{schedule.get_schedule_tomorrow_text()}", parse_mode="HTML")


async def command_schedule_yesterday(message: types.Message):
    await message.reply(f"{emojize(':calendar:')} <b>Расписание матчей:</b>\n{schedule.get_schedule_yesterday_text()}", parse_mode="HTML")


async def command_gameday(message: types.Message):
    await message.answer(f"#GameDay - {schedule.get_schedule_today_text()}", parse_mode="HTML")


async def command_schedule_team(message: types.Message):
    await message.reply(f"{emojize(':calendar:')} <b>Расписание матчей любимых команд:</b>\n{schedule.get_schedule_user_teams(message.from_user)}", parse_mode="HTML")


def register_handlers_schedule(dp : Dispatcher):
    dp.register_message_handler(command_scores, commands=['scores'])
    dp.register_message_handler(command_schedule, commands=['schedule'])
    dp.register_message_handler(command_schedule_today, commands=['today'])
    dp.register_message_handler(command_schedule_tomorrow, commands=['tomorrow'])
    dp.register_message_handler(command_schedule_yesterday, commands=['yesterday'])
    dp.register_message_handler(command_gameday, commands=['gameday'])
