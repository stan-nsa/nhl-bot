# Schedule:  https://statsapi.web.nhl.com/api/v1/schedule?expand=schedule.teams,schedule.scoringplays,schedule.game.seriesSummary,seriesSummary.series,schedule.linescore
#            https://statsapi.web.nhl.com/api/v1/schedule?date=2022-11-25
# Standings: https://statsapi.web.nhl.com/api/v1/standings
# Boxscore:  https://statsapi.web.nhl.com/api/v1/game/2021021092/boxscore

# All players: https://records.nhl.com/site/api/player/


import requests
from datetime import datetime, timezone, date, timedelta
import pytz
from emoji import emojize #Overview of all emoji: https://carpedm20.github.io/emoji/
import db

NHL_API_URL = "https://statsapi.web.nhl.com/api/v1"

# TimeZone
tzEST = pytz.timezone("US/Eastern")
tzMSK = pytz.timezone("Europe/Moscow")
tzVLAT = pytz.timezone("Asia/Vladivostok")


def get_request_nhl_api(query_str):
    response = requests.get(NHL_API_URL + query_str, params={"Content-Type": "application/json"})
    return response.json()


def get_teams():
    teams_str = '/teams'

    data = get_request_nhl_api(teams_str)

    return data['teams']


def get_teams_for_settings():
    teams = get_teams()
    txt = ""
    for team in teams:
        txt += f"{team['name']}\n"

    return txt


def get_schedule_day(data):
    # loop through dates
    txt = ""
    for date_day in data['dates']:

        txt += f"\n{emojize(':calendar:')} <b>{date_day['date']}:</b>\n"

        for game in date_day['games']:
            # Scheduled
            if int(game['status']['statusCode']) < 3:# 1 - Scheduled; 2 - Pre-Game
                txt += f"{game['teams']['away']['team']['abbreviation']}{emojize(':ice_hockey:')}{game['teams']['home']['team']['abbreviation']} " \
                       f"{emojize(':alarm_clock:')} {get_game_time_tz_text(game['gameDate'])}\n"
            # Live
            elif int(game['status']['statusCode']) < 5:# 3 - Live/In Progress; 4 - Live/In Progress - Critical
                txt += f"{get_game_teams_score(game['teams'], game['status'])} - {emojize(':green_circle:')} {game['linescore']['currentPeriodOrdinal']}\n"
            # Final
            elif int(game['status']['statusCode']) < 8:# 5 - Final/Game Over; 6 - Final; 7 - Final
                txt += f"{get_game_teams_score(game['teams'], game['status'])} - {emojize(':chequered_flag:')} " \
                       f"{'' if game['linescore']['currentPeriod']==3 else game['linescore']['currentPeriodOrdinal']}\n"
            # TBD/Postponed
            elif int(game['status']['statusCode']) < 10:# 8 - Scheduled (Time TBD); 9 - Postponed
                txt += f"{game['teams']['away']['team']['abbreviation']}{emojize(':ice_hockey:')}{game['teams']['home']['team']['abbreviation']} " \
                       f"{emojize(':stop_sign:')} {game['status']['detailedState']}\n"
            # Other
            else:
                txt += f"{game['teams']['away']['team']['abbreviation']}{emojize(':ice_hockey:')}{game['teams']['home']['team']['abbreviation']}\n"

    return txt


def get_standings():
    standings_str = "/standings"

    data = get_request_nhl_api(standings_str)

    return data['records']


def get_standings_text(full=False):
    data = get_standings()

    txt = "<pre>"
    in_po_symbol = '*'
    #in_po_symbol = emojize(':star:')
    for div in data:
        if (full):
            txt += f"\n#|{div['division']['name'].center(22, '_')}|Pt|GP|W-L-O\n"
        else:
            txt += f"\n#|{div['division']['name'].center(22, '_')}|Pt|GP\n"

        for team in div['teamRecords']:
            in_po = in_po_symbol if (int(team['wildCardRank']) < 3) else (' ')
            if (full):
                txt += f"{team['divisionRank']}|{team['team']['name'].ljust(21, ' ')}{in_po}|{team['points']}|{team['gamesPlayed']}|{team['leagueRecord']['wins']}-{team['leagueRecord']['losses']}-{team['leagueRecord']['ot']}\n"
            else:
                txt += f"{team['divisionRank']}|{team['team']['name'].ljust(21, ' ')}{in_po}|{team['points']}|{team['gamesPlayed']}\n"

    return txt + "</pre>"


def get_scores():

    schedule_str = "/schedule?expand=schedule.teams,schedule.linescore"
    #schedule_str = "/schedule?expand=schedule.teams,schedule.linescore&date=2022-11-26"
    #schedule_str = "/schedule?expand=schedule.teams,schedule.linescore&date=2022-11-23"

    data = get_request_nhl_api(schedule_str)

    return data


def get_scores_text():
    data = get_scores()
    # loop through dates
    txt = ""
    for date_day in data['dates']:

        #txt += f"\n{emojize(':calendar:')} <b>{date_day['date']}:</b>\n"
        txt += f"\n{emojize(':calendar:')} {date_day['date']}|EST|MSK|KHV\n"

        for game in date_day['games']:
            # Scheduled
            if int(game['status']['statusCode']) < 3:# 1 - Scheduled; 2 - Pre-Game
                txt += f"{game['teams']['away']['team']['abbreviation']}{emojize(':ice_hockey:')}{game['teams']['home']['team']['abbreviation']} " \
                       f"{emojize(':alarm_clock:')} {get_game_time_tz_text(game['gameDate'])}\n"
            # Live
            elif int(game['status']['statusCode']) < 5:# 3 - Live/In Progress; 4 - Live/In Progress - Critical
                txt += f"{get_game_teams_score(game['teams'], game['status'])} - {emojize(':green_circle:')} {game['linescore']['currentPeriodOrdinal']}\n"
            # Final
            elif int(game['status']['statusCode']) < 8:# 5 - Final/Game Over; 6 - Final; 7 - Final
                txt += f"{get_game_teams_score(game['teams'], game['status'])} - {emojize(':chequered_flag:')} " \
                       f"{'' if game['linescore']['currentPeriod']==3 else game['linescore']['currentPeriodOrdinal']}\n"
            # TBD/Postponed
            elif int(game['status']['statusCode']) < 10:# 8 - Scheduled (Time TBD); 9 - Postponed
                txt += f"{game['teams']['away']['team']['abbreviation']}{emojize(':ice_hockey:')}{game['teams']['home']['team']['abbreviation']} " \
                       f"{emojize(':stop_sign:')} {game['status']['detailedState']}\n"
            # Other
            else:
                txt += f"{game['teams']['away']['team']['abbreviation']}{emojize(':ice_hockey:')}{game['teams']['home']['team']['abbreviation']}\n"

    return txt




def get_results_today():

    schedule_str = "/schedule?expand=schedule.teams,schedule.linescore"
    #schedule_str = "/schedule?expand=schedule.teams,schedule.linescore&date=2022-11-26"
    #schedule_str = "/schedule?expand=schedule.teams,schedule.linescore&date=2022-11-23"

    data = get_request_nhl_api(schedule_str)

    txt = get_schedule_day(data)

    return txt


def get_schedule_today():

    schedule_str = "/schedule?expand=schedule.teams,schedule.linescore"
    #schedule_str = "/schedule?expand=schedule.teams,schedule.linescore&date=2022-11-26"
    #schedule_str = "/schedule?expand=schedule.teams,schedule.linescore&date=2022-11-23"

    schedule_str += f"&date={date.today().strftime('%Y-%m-%d')}"

    data = get_request_nhl_api(schedule_str)

    txt = get_schedule_day(data)

    return txt


def get_schedule_tomorrow():

    schedule_str = "/schedule?expand=schedule.teams,schedule.linescore"
    #schedule_str = "/schedule?expand=schedule.teams,schedule.linescore&date=2022-11-26"
    #schedule_str = "/schedule?expand=schedule.teams,schedule.linescore&date=2022-11-23"

    schedule_str += f"&date={(date.today() + timedelta(days=1)).strftime('%Y-%m-%d')}"

    data = get_request_nhl_api(schedule_str)

    txt = get_schedule_day(data)

    return txt


def get_schedule_yesterday():

    schedule_str = "/schedule?expand=schedule.teams,schedule.linescore"
    #schedule_str = "/schedule?expand=schedule.teams,schedule.linescore&date=2022-11-26"
    #schedule_str = "/schedule?expand=schedule.teams,schedule.linescore&date=2022-11-23"

    schedule_str += f"&date={(date.today() - timedelta(days=1)).strftime('%Y-%m-%d')}"

    data = get_request_nhl_api(schedule_str)

    txt = get_schedule_day(data)

    return txt


def get_schedule_user_teams(user):

    schedule_str = "/schedule?expand=schedule.teams,schedule.linescore"

    schedule_str += f"&startDate={(date.today() + timedelta(days=-5)).strftime('%Y-%m-%d')}"
    schedule_str += f"&endDate={(date.today() + timedelta(days=5)).strftime('%Y-%m-%d')}"

    schedule_str += "&teamId="

    user_teams = db.get_user_favorites_teams(user)
    for team in user_teams:
        schedule_str += f"{team[0]},"

    data = get_request_nhl_api(schedule_str)

    txt = get_schedule_day(data)

    return txt


def get_game_time_tz_text(dt_str, withTZ=True):

    dt = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)

    dtEST = dt.astimezone(tzEST)
    dtMSK = dt.astimezone(tzMSK)
    dtVLAT = dt.astimezone(tzVLAT)

    ft = "%H:%M %Z" if (withTZ) else "%H:%M"
    str = f"{dtEST.strftime(ft)} / {dtMSK.strftime(ft)} / {dtVLAT.strftime(ft).replace('+10', 'KHV')}"

    return str


def get_game_teams_score(game_teams, game_status):

    away_team = "<code>" + game_teams['away']['team']['abbreviation'] + "</code>"
    #away_team = game_teams['away']['team']['abbreviation']
    away_team_score = game_teams['away']['score']

    home_team = "<code>" + game_teams['home']['team']['abbreviation'] + "</code>"
    #home_team = game_teams['home']['team']['abbreviation']
    home_team_score = game_teams['home']['score']

    game_teams_score = f"{away_team} {str(get_game_team_score(away_team_score))}{emojize(':ice_hockey:')}{str(get_game_team_score(home_team_score))} {home_team}"

    return game_teams_score


def get_game_team_score(game_team_score, emoji=True):

    if emoji:
        game_team_score = emojize(f":keycap_{game_team_score}:") if (game_team_score <= 10) else emojize(f":keycap_{game_team_score//10}::keycap_{game_team_score%10}:")

    game_team_score = f"<tg-spoiler>{game_team_score}</tg-spoiler>"

    return game_team_score


#print(get_schedule_today())

