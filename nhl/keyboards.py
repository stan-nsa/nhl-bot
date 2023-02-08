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


#-- Keyboard for Stats ----------------------------------------------------------------------------
def keyboard_stats_goalies():
    kb = InlineKeyboardMarkup().row(InlineKeyboardButton("GGA", callback_data="stats_goalies_goalsAgainstAverage_ASC"),
                                    InlineKeyboardButton("Save %", callback_data="stats_goalies_savePct_DESC"),
                                    InlineKeyboardButton("Shutouts", callback_data="stats_goalies_shutouts_DESC"),
                                    InlineKeyboardButton("Wins", callback_data="stats_goalies_wins_DESC"))

    return kb


def keyboard_stats_skaters():
    kb = InlineKeyboardMarkup().row(InlineKeyboardButton("Points", callback_data="stats_skaters_points"),
                                    InlineKeyboardButton("Goals", callback_data="stats_skaters_goals"),
                                    InlineKeyboardButton("Assists", callback_data="stats_skaters_assists"))

    return kb


def keyboard_stats_defensemen():
    kb = InlineKeyboardMarkup().row(InlineKeyboardButton("Points", callback_data="stats_defensemen_points"),
                                    InlineKeyboardButton("Goals", callback_data="stats_defensemen_goals"),
                                    InlineKeyboardButton("Assists", callback_data="stats_defensemen_assists"))

    return kb


def keyboard_stats_rookies():
    kb = InlineKeyboardMarkup().row(InlineKeyboardButton("Points", callback_data="stats_rookies_points"),
                                    InlineKeyboardButton("Goals", callback_data="stats_rookies_goals"),
                                    InlineKeyboardButton("Assists", callback_data="stats_rookies_assists"))

    return kb


def keyboard_stats_teams():
    kb = InlineKeyboardMarkup().row(InlineKeyboardButton("Wins", callback_data="stats_teams_wins_DESC"),
                                    InlineKeyboardButton("PP %", callback_data="stats_teams_powerPlayPct_DESC"),
                                    InlineKeyboardButton("PK %", callback_data="stats_teams_penaltyKillPct_DESC"))

    return kb

