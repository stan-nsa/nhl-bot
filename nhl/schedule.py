from datetime import datetime, timezone, date, timedelta
from emoji import emojize #Overview of all emoji: https://carpedm20.github.io/emoji/
from nhl import nhl
from db import db

import pytz


# TimeZone
tzEST = pytz.timezone("US/Eastern")
tzMSK = pytz.timezone("Europe/Moscow")
tzVLAT = pytz.timezone("Asia/Vladivostok")

# Дата для инлайн кнопок
CurrentDate = ''


#== Получение от сервера данных расписания ========================================================

# Получение от сервера данных расписания для инлайн-меню
def get_schedule_dates_for_inlinemenu(day=None):

    dates = {'day': '', 'previous': '', 'next': ''}
    days_delta = 10

    schedule_str = "/schedule"

    if (day == None):
        data = nhl.get_request_nhl_api(schedule_str)

        dates['day'] = date.fromisoformat(data['dates'][0]['date']) if (data['totalItems'] > 0) else \
                       datetime.strptime(data['metaData']['timeStamp'], "%Y%m%d_%H%M%S").replace(tzinfo=timezone.utc).astimezone(tzEST)
    else:
        dates['day'] = date.fromisoformat(day)

    dates['previous'] = dates['day'] + timedelta(days=-1)
    data = nhl.get_request_nhl_api(schedule_str + f"?startDate={(dates['previous'] + timedelta(days=-days_delta)).strftime('%Y-%m-%d')}&endDate={dates['previous'].strftime('%Y-%m-%d')}")
    dates['previous'] = data['dates'][len(data['dates']) - 1]['date'] if (data['totalItems'] > 0) else ''

    dates['next'] = dates['day'] + timedelta(days=+1)
    data = nhl.get_request_nhl_api(schedule_str + f"?startDate={dates['next'].strftime('%Y-%m-%d')}&endDate={(dates['next'] + timedelta(days=+days_delta)).strftime('%Y-%m-%d')}")
    dates['next'] = data['dates'][0]['date'] if (data['totalItems'] > 0) else ''

    dates['day'] = dates['day'].strftime('%Y-%m-%d')

    return dates


# Получение от сервера данных расписания на день ('%Y-%m-%d')
def get_schedule_data_day(day=None):

    schedule_str = "/schedule?expand=schedule.teams,schedule.linescore"

    schedule_str += f"&date={day}" if (day != None) else ''

    data = nhl.get_request_nhl_api(schedule_str)

    return data


# Формирование теста для вывода расписания на день ('%Y-%m-%d')
def get_schedule_day_text(day=None):
    data = get_schedule_data_day(day)

    txt = get_schedule_days_text(data)

    return txt


# Получение от сервера данных расписания на завтра
def get_schedule_tomorrow():

    schedule_str = "/schedule?expand=schedule.teams,schedule.linescore"
    #schedule_str = "/schedule?expand=schedule.teams,schedule.linescore&date=2022-11-26"
    #schedule_str = "/schedule?expand=schedule.teams,schedule.linescore&date=2022-11-23"

    schedule_str += f"&date={(date.today() + timedelta(days=1)).strftime('%Y-%m-%d')}"

    data = nhl.get_request_nhl_api(schedule_str)

    return data


# Формирование теста для вывода расписания на завтра
def get_schedule_tomorrow_text():
    data = get_schedule_tomorrow()

    txt = get_schedule_days_text(data)

    return txt


# Получение от сервера данных расписания за вчера
def get_schedule_yesterday():

    schedule_str = "/schedule?expand=schedule.teams,schedule.linescore"
    #schedule_str = "/schedule?expand=schedule.teams,schedule.linescore&date=2022-11-26"
    #schedule_str = "/schedule?expand=schedule.teams,schedule.linescore&date=2022-11-23"

    schedule_str += f"&date={(date.today() - timedelta(days=1)).strftime('%Y-%m-%d')}"

    data = nhl.get_request_nhl_api(schedule_str)

    return data


# Формирование теста для вывода расписания за вчера
def get_schedule_yesterday_text():
    data = get_schedule_yesterday()

    txt = get_schedule_days_text(data)

    return txt


# Формирование теста для вывода расписания за один день
def get_schedule_days_text(data):
    # loop through dates
    txt = ""
    for date_day in data['dates']:

        # txt += f"\n{emojize(':calendar:')} <b>{date_day['date']}:</b>\n"
        #txt += f"\n{emojize(':calendar:')} <b>{date_day['date']}{emojize(':alarm_clock:')}EST|MSK|KHV</b>\n"
        txt += f"\n{emojize(':calendar:')} <b>{date_day['date']}:</b>\n" \
               f"<code>___{emojize(':ice_hockey:')}___{emojize(':alarm_clock:')}_EST_|_MSK_|_KHV_</code>\n"

        for game in date_day['games']:
            # Scheduled
            if int(game['status']['statusCode']) < 3:  # 1 - Scheduled; 2 - Pre-Game
                txt += f"<code>{game['teams']['away']['team']['abbreviation']}{emojize(':ice_hockey:')}{game['teams']['home']['team']['abbreviation']}" \
                       f"{emojize(':alarm_clock:')}{get_game_time_tz_text(game['gameDate'])}</code>\n"
            # Live
            elif int(game['status']['statusCode']) < 5:  # 3 - Live/In Progress; 4 - Live/In Progress - Critical
                txt += f"{get_game_teams_score_text(game['teams'], game['status'])} - {emojize(':green_circle:')} {game['linescore']['currentPeriodOrdinal']}\n"
            # Final
            elif int(game['status']['statusCode']) < 8:  # 5 - Final/Game Over; 6 - Final; 7 - Final
                txt += f"{get_game_teams_score_text(game['teams'], game['status'])} - {emojize(':chequered_flag:')} " \
                       f"{'' if game['linescore']['currentPeriod'] == 3 else game['linescore']['currentPeriodOrdinal']}\n"
            # TBD/Postponed
            elif int(game['status']['statusCode']) < 10:  # 8 - Scheduled (Time TBD); 9 - Postponed
                txt += f"{game['teams']['away']['team']['abbreviation']}{emojize(':ice_hockey:')}{game['teams']['home']['team']['abbreviation']} " \
                       f"{emojize(':stop_sign:')} {game['status']['detailedState']}\n"
            # Other
            else:
                txt += f"{game['teams']['away']['team']['abbreviation']}{emojize(':ice_hockey:')}{game['teams']['home']['team']['abbreviation']}\n"

    return txt


def get_game_teams_score_text(game_teams, game_status):

    away_team = "<code>" + game_teams['away']['team']['abbreviation'] + "</code>"
    #away_team = game_teams['away']['team']['abbreviation']
    away_team_score = game_teams['away']['score']

    home_team = "<code>" + game_teams['home']['team']['abbreviation'] + "</code>"
    #home_team = game_teams['home']['team']['abbreviation']
    home_team_score = game_teams['home']['score']

    game_teams_score = f"{away_team} {str(get_game_team_score_text(away_team_score))}{emojize(':ice_hockey:')}{str(get_game_team_score_text(home_team_score))} {home_team}"

    return game_teams_score


def get_game_team_score_text(game_team_score, emoji=True):

    if emoji:
        game_team_score = emojize(f":keycap_{game_team_score}:") if (game_team_score <= 10) else emojize(f":keycap_{game_team_score//10}::keycap_{game_team_score%10}:")

    game_team_score = f"<tg-spoiler>{game_team_score}</tg-spoiler>"

    return game_team_score


#== Получение от сервера данных результатов матчей ================================================

# Получение от сервера данных текущих результатов матчей
def get_scores():

    schedule_str = "/schedule?expand=schedule.teams,schedule.linescore"
    #schedule_str = "/schedule?expand=schedule.teams,schedule.linescore&date=2022-11-26"
    #schedule_str = "/schedule?expand=schedule.teams,schedule.linescore&date=2022-11-23"

    data = nhl.get_request_nhl_api(schedule_str)

    return data


# Формирование теста для вывода текущих результатов матчей
def get_scores_text(data=None):
    data = get_scores() if (data==None) else data

    txt = get_schedule_days_text(data)

    return txt





def get_schedule_user_teams(user):

    schedule_str = "/schedule?expand=schedule.teams,schedule.linescore"

    schedule_str += f"&startDate={(date.today() + timedelta(days=-5)).strftime('%Y-%m-%d')}"
    schedule_str += f"&endDate={(date.today() + timedelta(days=5)).strftime('%Y-%m-%d')}"

    schedule_str += "&teamId="

    user_teams = db.get_user_favorites_teams(user)
    for team in user_teams:
        schedule_str += f"{team[0]},"

    data = nhl.get_request_nhl_api(schedule_str)

    txt = get_schedule_days_text(data)

    return txt


def get_game_time_tz_text(dt_str, withTZ=True):
    withTZ = False
    dt = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)

    dtEST = dt.astimezone(tzEST)
    dtMSK = dt.astimezone(tzMSK)
    dtVLAT = dt.astimezone(tzVLAT)

    ft = "%H:%M %Z" if (withTZ) else "%H:%M"
    str = f"{dtEST.strftime(ft)}|{dtMSK.strftime(ft)}|{dtVLAT.strftime(ft).replace('+10', 'KHV')}".lower()

    return str

