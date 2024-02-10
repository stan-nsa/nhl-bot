from aiogram import types, Dispatcher, exceptions
from aiogram.dispatcher.filters import Text

from nhl import nhl
from nhl import game
from nhl import keyboards


async def command_game_details(callback : types.CallbackQuery):
    game_id, details = callback.data.split('_')[2:]

    if details == 'button':
        func = callback.message.answer
        details = 'scoring'
    else:
        func = callback.message.edit_text

    txt = f"{nhl.ico['hockey']} <b>Game:</b>\n{game.get_game_text(game_id, details)}"

    try:
        await func(txt, parse_mode="HTML", reply_markup=keyboards.keyboard_game_details(game_id))

    except exceptions.MessageNotModified:
        pass

    finally:
        await callback.answer()


def register_handlers_game(dp: Dispatcher):
    dp.register_callback_query_handler(command_game_details, Text(startswith='Game_Details'))
