# Schedule:  https://statsapi.web.nhl.com/api/v1/schedule?expand=schedule.teams,schedule.scoringplays,schedule.game.seriesSummary,seriesSummary.series,schedule.linescore
#            https://statsapi.web.nhl.com/api/v1/schedule?date=2022-11-25
# https://api-web.nhle.com/v1/gamecenter/2023020206/landing


from datetime import datetime, timezone, date, timedelta
from emoji import emojize #Overview of all emoji: https://carpedm20.github.io/emoji/
from nhl import nhl
from db import db


#== Получение от сервера данных расписания ========================================================

# Получение от сервера данных расписания для инлайн-меню
def get_schedule_dates_for_inlinemenu(day=None):

    dates = {'previous': '', 'day': '', 'next': ''}

    data = get_schedule_day_data(day)

    dates['previous'] = data['prevDate']
    dates['next'] = data['nextDate']
    dates['day'] = data['currentDate']

    return dates


# Получение от сервера данных расписания на день для инлайн-меню
def get_schedule_day_games_for_inlinemenu(day=None, data=None):
    data = get_schedule_day_data(day) if (data is None) else data

    games = []

    for game in data['games']:

        txt = get_schedule_game_text(game, inlinemenu=True)

        # Play-off series Summary
        #txt += f" ({game['seriesSummary']['gameLabel'].replace('ame ', '#')} {game['seriesSummary']['seriesStatusShort']})" if (game['gameType'] == "P") else ""

        games.append({'id': game['id'], 'text': txt})

    return games


# Получение от сервера данных расписания на день ('%Y-%m-%d')
def get_schedule_day_data(day=None):

    schedule_str = f"score/" + (day if (day is not None) else 'now')

    data = nhl.get_request_nhl_api(schedule_str)

    return data


# Формирование теста для вывода расписания на день ('%Y-%m-%d')
def get_schedule_day_text(day=None, data=None, hideScore=False):
    data = get_schedule_day_data(day) if (data is None) else data

    txt = get_schedule_days_text(data, hideScore=hideScore)

    return txt


# Формирование теста для вывода расписания
def get_schedule_days_text(data, hideScore=False):

    txt = f"\n{nhl.ico['schedule']} <b>{data['currentDate']}:</b>\n"

    header_live = ''
    header_scheduled = ''
    header_finished = ''
    for game in data['games']:
        # Scheduled
        if game['gameState'] in nhl.gameState['scheduled']:
            if (header_scheduled == ''): # Заголовок таблицы расписания
                header_scheduled = \
                    f"\n{nhl.ico['time']} <b>Scheduled:</b>\n" \
                    f"<code>___{nhl.ico['vs']}___{nhl.ico['time']}_EST_|_MSK_|_KHV_</code>\n"
                txt += header_scheduled

        # Live
        elif game['gameState'] in nhl.gameState['live']:
            if (header_live == ''):
                header_live = f"\n{nhl.ico['live']} <b>Live:</b>\n"
                txt += header_live

        # Final
        elif game['gameState'] in nhl.gameState['final']:
            if (header_finished == ''):
                header_finished = f"\n{nhl.ico['finished']} <b>Finished:</b>\n"
                txt += header_finished

        txt += get_schedule_game_text(game, hideScore=hideScore) + "\n"

    return txt


# Формирование теста для вывода сведений об игре
def get_schedule_game_text(game, hideScore=False, inlinemenu=False):

    # Scheduled
    if game['gameState'] in nhl.gameState['scheduled']:
        txt = f"{game['awayTeam']['abbrev']}{nhl.ico['vs']}{game['homeTeam']['abbrev']}" \
               f"{nhl.ico['time']}{get_game_time_tz_text(game['startTimeUTC'], inlinemenu=inlinemenu)}"
        txt = txt if (inlinemenu) else f"<code>{txt}</code>"

    # Live
    elif game['gameState'] in nhl.gameState['live']:
        currentPeriod = game['periodDescriptor']['periodType'] if game['periodDescriptor']['number'] > 3 else nhl.gamePeriods[game['periodDescriptor']['number']]
        txt = f"{get_game_teams_score_text(game, hideScore=hideScore, inlinemenu=inlinemenu)} - " \
              f"{nhl.ico['live']} {currentPeriod}/" \
              f"{'END' if (game['clock']['inIntermission']) else game['clock']['timeRemaining']}"

    # Final
    elif game['gameState'] in nhl.gameState['final']:
        teams_score_text = get_game_teams_score_text(game, hideScore=hideScore, inlinemenu=inlinemenu)
        txt = f"{teams_score_text} - " \
               f"{nhl.ico['finished']} {'' if game['periodDescriptor']['number'] == 3 else game['periodDescriptor']['periodType']}"

    # TBD/Postponed
    elif game['gameState'] in nhl.gameState['tbd']:  # 8 - Scheduled (Time TBD); 9 - Postponed
        txt = f"{game['awayTeam']['abbrev']}{nhl.ico['vs']}{game['homeTeam']['abbrev']}" \
               f"{nhl.ico['tbd']} {game['gameState']}"
        txt = txt if (inlinemenu) else f"<code>{txt}</code>"

    # Other
    else:
        txt = f"{game['awayTeam']['abbrev']}{nhl.ico['vs']}{game['homeTeam']['abbrev']}"
        txt = txt if (inlinemenu) else f"<code>{txt}</code>"

    return txt


def get_game_teams_score_text(game, hideScore=False, inlinemenu=False):

    away_team = game['awayTeam']['abbrev'] if (inlinemenu) else f"<code>{game['awayTeam']['abbrev']}</code>"
    away_team_score = game['awayTeam']['score']

    home_team = game['homeTeam']['abbrev'] if (inlinemenu) else f"<code>{game['homeTeam']['abbrev']}</code>"
    home_team_score = game['homeTeam']['score']

    game_teams_score = f"{away_team} {get_game_team_score_text(away_team_score, hideScore=hideScore)}{nhl.ico['vs']}{get_game_team_score_text(home_team_score, hideScore=hideScore)} {home_team}"

    return game_teams_score


def get_game_team_score_text(game_team_score, emoji=True, hideScore=False):

    if emoji:
        game_team_score = emojize(f":keycap_{game_team_score}:") if (game_team_score <= 10) else emojize(f":keycap_{game_team_score//10}::keycap_{game_team_score%10}:")

    game_team_score = f"<tg-spoiler>{game_team_score}</tg-spoiler>" if (hideScore) else f"{game_team_score}"

    return game_team_score


#== Получение от сервера данных результатов матчей ================================================

# Получение от сервера данных текущих результатов матчей
def get_scores():

    data = get_schedule_day_data()

    return data


# Формирование теста для вывода текущих результатов матчей
def get_scores_text(data=None, hideScore=True):
    data = get_scores() if (data is None) else data

    txt = get_schedule_days_text(data, hideScore=hideScore)

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


def get_game_time_tz_text(dt_str, withDate=False, withTZ=False, inlinemenu=False):

    dt = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)

    dtEST = dt.astimezone(nhl.tz['EST'])
    dtMSK = dt.astimezone(nhl.tz['MSK'])
    dtKHV = dt.astimezone(nhl.tz['KHV'])

    str = f"{dtEST.date().isoformat()} {nhl.ico['time']} " if (withDate) else ''

    ft = "%H:%M %Z" if (withTZ or inlinemenu) else "%H:%M"
    str += f"{dtEST.strftime(ft)}|{dtMSK.strftime(ft)}|{dtKHV.strftime(ft).replace('+10', 'KHV')}".upper() #lower()

    str = str if (inlinemenu) else f"<code>{str}</code>"

    return str


# Получение корректной даты, если получены пустые данные
def get_correct_date_from_data(data, as_str=True):
    if (data['totalItems'] > 0):
        day = data['dates'][0]['date'] if (as_str) else date.fromisoformat(data['dates'][0]['date'])
    else:
        day = datetime.strptime(data['metaData']['timeStamp'], "%Y%m%d_%H%M%S").replace(tzinfo=timezone.utc).astimezone(nhl.tz['EST'])
        day = day.date().isoformat() if (as_str) else day

    return day

def get_schedule_data_by_dame_for_leagueRecords(game_id: str):
    schedule_str = f"/schedule?expand=schedule.leagueRecord,schedule.game.seriesSummary&gamePk={game_id}"

    data = nhl.get_request_nhl_api(schedule_str)

    return data

