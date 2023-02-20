from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from nhl import nhl
from nhl import game
from nhl import keyboards


async def command_game_details(callback : types.CallbackQuery):
    callback_data_parts = callback.data.split('_')
    game_id = callback_data_parts[2]

    if (len(callback_data_parts) < 4):
        details = 'scoringPlays'
        await callback.message.answer(
            f"{nhl.ico['hockey']} <b>Game:</b>\n{game.get_game_text(game_id, details)}", parse_mode="HTML",
            reply_markup=keyboards.keyboard_game_details(game_id))
        await callback.answer()

    else:
        details = callback_data_parts[3]
        await callback.message.edit_text(
            f"{nhl.ico['hockey']} <b>Game:</b>\n{game.get_game_text(game_id, details)}", parse_mode="HTML",
            reply_markup=keyboards.keyboard_game_details(game_id))
        await callback.answer(f"Game: {game_id} updated!")


def register_handlers_game(dp: Dispatcher):
    dp.register_callback_query_handler(command_game_details, Text(startswith='Game_Details'))
