from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from emoji import emojize #Overview of all emoji: https://carpedm20.github.io/emoji/

from nhl import game
from nhl import keyboards


async def command_scores_game_details(callback : types.CallbackQuery):
    callback_data_parts = callback.data.split('_')
    game_id = callback_data_parts[4]

    await callback.message.answer(
        f"{emojize(':goal_net::ice_hockey:')} <b>Scores:</b>\n{game.get_game_text(game_id)}", parse_mode="HTML",
        reply_markup=keyboards.keyboard_game_details(game_id))

    await callback.answer()


async def command_game_details(callback : types.CallbackQuery):
    callback_data_parts = callback.data.split('_')
    game_id = callback_data_parts[2]
    details = callback_data_parts[3]

    await callback.message.answer(
        f"{emojize(':goal_net::ice_hockey:')} <b>Scores:</b>\n{game.get_game_text(game_id, details)}", parse_mode="HTML",
        reply_markup=keyboards.keyboard_game_details(game_id))

    await callback.answer()


def register_handlers_game(dp: Dispatcher):
    dp.register_callback_query_handler(command_scores_game_details, Text(startswith='schedule_scores_game_details'))
    dp.register_callback_query_handler(command_game_details, Text(startswith='game_details'))
