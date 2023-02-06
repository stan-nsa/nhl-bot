from aiogram import types, Dispatcher
from nhl import nhl

from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def command_standings(message: types.Message):
    await message.reply(f"<b>Турнирная таблица:</b>\n{nhl.get_standings_text(full=False)}", parse_mode="HTML",
                        reply_markup=InlineKeyboardMarkup().row(InlineKeyboardButton("Division", callback_data="standings_byDivision"),
                                                                InlineKeyboardButton("Wild Card", callback_data="standings_wildCardWithLeaders"),
                                                                InlineKeyboardButton("League", callback_data="standings_byLeague")))


async def command_standings_type(callback : types.CallbackQuery):
    standings_type = callback.data.split('_')[1]
    await callback.message.answer(f"<b>Турнирная таблица:</b>\n{nhl.get_standings_text(standings_type, full=False)}", parse_mode="HTML",
                                  reply_markup=InlineKeyboardMarkup().row(InlineKeyboardButton("Division", callback_data="standings_byDivision"),
                                                                          InlineKeyboardButton("Wild Card", callback_data="standings_wildCardWithLeaders"),
                                                                          InlineKeyboardButton("League", callback_data="standings_byLeague")))
    await callback.answer()


def register_handlers_nhl(dp : Dispatcher):
    dp.register_message_handler(command_standings, commands=['standings'])
    dp.register_callback_query_handler(command_standings_type, Text(startswith='standings_'))

