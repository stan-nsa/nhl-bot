from aiogram import types
from emoji import emojize #Overview of all emoji: https://carpedm20.github.io/emoji/
from create_bot import dp

import nhl

@dp.message_handler(commands=['gameday'])
async def send_schedule_gameday(message: types.Message):
    await message.answer(f"#GameDay - {emojize(':calendar:')} <b>Расписание матчей:</b>\n{nhl.get_schedule_today()}", parse_mode="HTML")


@dp.message_handler(commands=['schedule'])
async def send_schedule_team(message: types.Message):
    await message.reply(f"{emojize(':calendar:')} <b>Расписание матчей любимых команд:</b>\n{nhl.get_schedule_user_teams(message.from_user)}", parse_mode="HTML")


@dp.message_handler(commands=['today'])
async def send_schedule_today(message: types.Message):
    await message.reply(f"{emojize(':calendar:')} <b>Расписание матчей:</b>\n{nhl.get_schedule_today()}", parse_mode="HTML")


@dp.message_handler(commands=['tomorrow'])
async def send_schedule_today(message: types.Message):
    await message.reply(f"{emojize(':calendar:')} <b>Расписание матчей:</b>\n{nhl.get_schedule_tomorrow()}", parse_mode="HTML")


@dp.message_handler(commands=['yesterday'])
async def send_schedule_today(message: types.Message):
    await message.reply(f"{emojize(':calendar:')} <b>Расписание матчей:</b>\n{nhl.get_schedule_yesterday()}", parse_mode="HTML")


@dp.message_handler(commands=['results'])
async def send_results_today(message: types.Message):
    await message.reply(f"{emojize(':goal_net::ice_hockey:')} <b>Результаты матчей:</b>\n{nhl.get_results_today()}", parse_mode="HTML")

