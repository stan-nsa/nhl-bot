from emoji import emojize #Overview of all emoji: https://carpedm20.github.io/emoji/
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from nhl.nhl import ico

#-- Keyboard for Schedule -------------------------------------------------------------------------
def keyboard_scores(day):
    kb = keyboard_schedule(day=day)

    return kb


def keyboard_schedule(dates=None, day=None): # dates = {'day': '', 'previous': '', 'next': ''}, day = str('%Y-%m-%d')
    if (dates):
        kb = InlineKeyboardMarkup().row(InlineKeyboardButton(f"{dates['previous']} {ico['prev']}", callback_data=f"Schedule_day_{dates['previous']}"),
                                        InlineKeyboardButton(f"{ico['info']} Details", callback_data=f"Schedule_Details_day_{dates['day']}"),
                                        InlineKeyboardButton(f"{ico['next']} {dates['next']}", callback_data=f"Schedule_day_{dates['next']}"))
    else:
        kb = InlineKeyboardMarkup().row(InlineKeyboardButton(f"{ico['info']} Details", callback_data=f"Scores_Details_day_{day}"))

    return kb


def keyboard_schedule_details(games):
    kb = InlineKeyboardMarkup()

    for game in games:
        kb.add(InlineKeyboardButton(game['text'], callback_data=f"Game_Details_{game['id']}"))

    return kb


#-- Keyboard for Game -----------------------------------------------------------------------------
def keyboard_game_details(game_id):
    kb = InlineKeyboardMarkup().row(InlineKeyboardButton(f"{ico['stick']}{ico['goal']}Scoring", callback_data=f"Game_Details_{game_id}_scoringPlays"),
                                    InlineKeyboardButton(f"{ico['penalty']}Penalties", callback_data=f"Game_Details_{game_id}_penaltyPlays"),
                                    InlineKeyboardButton(f"{ico['stats']}Teams Stats", callback_data=f"Game_Details_{game_id}_teamsStats"))

    return kb


#-- Keyboard for Standings ------------------------------------------------------------------------
def keyboard_standings():
    kb = InlineKeyboardMarkup().row(InlineKeyboardButton("Division", callback_data="standings_byDivision"),
                                    InlineKeyboardButton("Wild Card", callback_data="standings_wildCardWithLeaders"),
                                    InlineKeyboardButton("League", callback_data="standings_byLeague"))

    return kb


#-- Keyboard for Stats ----------------------------------------------------------------------------
def keyboard_stats_gameType():
    kb = InlineKeyboardMarkup().row(InlineKeyboardButton("Regular season", callback_data="stats_leaders_regular"),
                                    InlineKeyboardButton("PlayOffs", callback_data="stats_leaders_playoff"))

    return kb


def keyboard_stats_goalies(gameType='regular'):
    kb = InlineKeyboardMarkup().row(InlineKeyboardButton("GGA", callback_data=f"stats_goalies_goalsAgainstAverage_ASC_{gameType}"),
                                    InlineKeyboardButton("Save %", callback_data=f"stats_goalies_savePct_DESC_{gameType}"),
                                    InlineKeyboardButton("Shutouts", callback_data=f"stats_goalies_shutouts_DESC_{gameType}"),
                                    InlineKeyboardButton("Wins", callback_data=f"stats_goalies_wins_DESC_{gameType}"))

    return kb


def keyboard_stats_skaters(gameType='regular'):
    kb = InlineKeyboardMarkup().row(InlineKeyboardButton("Points", callback_data=f"stats_skaters_points_{gameType}"),
                                    InlineKeyboardButton("Goals", callback_data=f"stats_skaters_goals_{gameType}"),
                                    InlineKeyboardButton("Assists", callback_data=f"stats_skaters_assists_{gameType}"))

    return kb


def keyboard_stats_defensemen(gameType='regular'):
    kb = InlineKeyboardMarkup().row(InlineKeyboardButton("Points", callback_data=f"stats_defensemen_points_{gameType}"),
                                    InlineKeyboardButton("Goals", callback_data=f"stats_defensemen_goals_{gameType}"),
                                    InlineKeyboardButton("Assists", callback_data=f"stats_defensemen_assists_{gameType}"))

    return kb


def keyboard_stats_rookies(gameType='regular'):
    kb = InlineKeyboardMarkup().row(InlineKeyboardButton("Points", callback_data=f"stats_rookies_points_{gameType}"),
                                    InlineKeyboardButton("Goals", callback_data=f"stats_rookies_goals_{gameType}"),
                                    InlineKeyboardButton("Assists", callback_data=f"stats_rookies_assists_{gameType}"))

    return kb


def keyboard_stats_teams_gameType():
    kb = InlineKeyboardMarkup().row(InlineKeyboardButton("Regular season", callback_data="stats_teams_regular"),
                                    InlineKeyboardButton("PlayOffs", callback_data="stats_teams_playoff"))

    return kb


def keyboard_stats_teams(gameType='regular'):
    kb = InlineKeyboardMarkup().row(InlineKeyboardButton("Wins", callback_data=f"stats_teams_wins_DESC_{gameType}"),
                                    InlineKeyboardButton("PP %", callback_data=f"stats_teams_powerPlayPct_DESC_{gameType}"),
                                    InlineKeyboardButton("PK %", callback_data=f"stats_teams_penaltyKillPct_DESC_{gameType}"))

    return kb

