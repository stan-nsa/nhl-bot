from aiogram import types, Dispatcher
from nhl import nhl
from nhl import keyboards

from aiogram.dispatcher.filters import Text


async def command_standings(message: types.Message):
    await message.answer(
        f"{nhl.ico['standings']}<b>Standings:</b>\n{nhl.get_standings_text(full=False)}",
        parse_mode="HTML",
        reply_markup=keyboards.keyboard_standings())


async def command_standings_type(callback: types.CallbackQuery):
    standings_type = callback.data.split('_')[1]
    try:
        #await callback.message.answer(
        await callback.message.edit_text(
            f"{nhl.ico['standings']}<b>Standings:</b>\n{nhl.get_standings_text(standings_type, full=False)}",
            parse_mode="HTML",
            reply_markup=keyboards.keyboard_standings())
        await callback.answer()

    except:
        await callback.answer()


def register_handlers_nhl(dp: Dispatcher):
    dp.register_message_handler(command_standings, commands=['standings'])
    dp.register_callback_query_handler(command_standings_type, Text(startswith='standings_'))

