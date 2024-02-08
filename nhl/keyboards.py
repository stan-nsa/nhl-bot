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
    kb = InlineKeyboardMarkup().row(InlineKeyboardButton(f"{ico['stick']}{ico['goal']}Scoring", callback_data=f"Game_Details_{game_id}_scoring"),
                                    InlineKeyboardButton(f"{ico['penalty']}Penalties", callback_data=f"Game_Details_{game_id}_penalties")).\
                                row(InlineKeyboardButton(f"{ico['stats']}Team Stats", callback_data=f"Game_Details_{game_id}_teamGameStats"),
                                    InlineKeyboardButton(f"{ico['report']}Game Reports", callback_data=f"Game_Details_{game_id}_gameReports"))

    return kb


#-- Keyboard for Standings ------------------------------------------------------------------------
def keyboard_standings():
    kb = InlineKeyboardMarkup().row(InlineKeyboardButton("Division", callback_data="standings_Division"),
                                    InlineKeyboardButton("Wild Card", callback_data="standings_WildCard"),
                                    InlineKeyboardButton("League", callback_data="standings_League"))

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


#-- Keyboard for Teams ----------------------------------------------------------------------------
def keyboard_teams(teams):
    kb = InlineKeyboardMarkup()

    for team in teams:
        teamName = team.get('teamName').get('default')
        teamAbbrev = team.get('teamAbbrev').get('default')
        kb.add(InlineKeyboardButton(teamName, callback_data=f"team_{teamAbbrev}:{teamName}_button"))

    # conferences = {'Eastern': {'Atlantic': [], 'Metropolitan': []},
    #                'Western': {'Central': [], 'Pacific': []}}
    #
    # for team in teams:
    #     conferences.get(team.get('conferenceName')).get(team.get('divisionName')).append(team)
    #
    # for c in conferences.values():
    #     for name, d in c.items():
    #         d = sorted(d, key=lambda d: d.get('divisionSequence'))
    #
    # for conf_name, conf in conferences.items():
    #     txt += f"\n<b>{conf_name}</b>\n"
    #     for div_name, div in conf.items():
    #         # txt += get_standings_table_header_text(caption=div_name, full=full)
    #         for team in div:
    #             n = team.get('wildcardSequence') if (div_name == 'WildCard') else team.get('divisionSequence')
    #             txt += get_standings_table_row_text(row=team, rank=n, full=full)

    return kb


def keyboard_team(teamAbbrev_teamName):
    kb = InlineKeyboardMarkup().row(InlineKeyboardButton(f"{ico['info']}Info", callback_data=f"team_{teamAbbrev_teamName}_info"),
                                    InlineKeyboardButton(f"{ico['stats']}Stats", callback_data=f"team_{teamAbbrev_teamName}_stats"),
                                    InlineKeyboardButton(f"{ico['schedule']}Schedule", callback_data=f"team_{teamAbbrev_teamName}_schedule"))

    return kb
