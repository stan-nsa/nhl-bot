from emoji import emojize #Overview of all emoji: https://carpedm20.github.io/emoji/
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

#-- Keyboard for Schedule -------------------------------------------------------------------------
def keyboard_schedule(dates): #dates = {'day': '', 'previous': '', 'next': ''}
    kb = InlineKeyboardMarkup().row(InlineKeyboardButton(f"{dates['previous']}{emojize(':left_arrow:')}", callback_data=f"schedule_day_{dates['previous']}"),
                                    InlineKeyboardButton(f"{dates['day']}", callback_data=f"schedule_day_{dates['day']}"),
                                    InlineKeyboardButton(f"{emojize(':right_arrow:')}{dates['next']}", callback_data=f"schedule_day_{dates['next']}"))

    return kb


#-- Keyboard for Standings ------------------------------------------------------------------------
def keyboard_standings():
    kb = InlineKeyboardMarkup().row(InlineKeyboardButton("Division", callback_data="standings_byDivision"),
                                    InlineKeyboardButton("Wild Card", callback_data="standings_wildCardWithLeaders"),
                                    InlineKeyboardButton("League", callback_data="standings_byLeague"))

    return kb

