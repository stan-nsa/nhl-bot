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

    dates['previous'] = data.get('prevDate')
    dates['next'] = data.get('nextDate')
    dates['day'] = data.get('currentDate')

    return dates


# Получение от сервера данных расписания на день для инлайн-меню
def get_schedule_day_games_for_inlinemenu(day=None, data=None):
    data = get_schedule_day_data(day) if (data is None) else data

    games = []

    for game in data.get('games'):

        txt = get_schedule_game_text(game, inlinemenu=True)

        # Play-off series Summary
        #txt += f" ({game.get('seriesSummary').get('gameLabel').replace('ame ', '#')} {game.get('seriesSummary').get('seriesStatusShort')})" if (game.get('gameType') == "P") else ""

        games.append({'id': game.get('id'), 'text': txt})

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

    txt = f"\n{nhl.ico.get('schedule')} <b>{data.get('currentDate')}:</b>\n"

    header_live = ''
    header_scheduled = ''
    header_finished = ''
    for game in data.get('games'):
        # Scheduled
        if game.get('gameState') in nhl.gameState.get('scheduled'):
            if (header_scheduled == ''): # Заголовок таблицы расписания
                header_scheduled = \
                    f"\n{nhl.ico.get('time')} <b>Scheduled:</b>\n" \
                    f"<code>___{nhl.ico.get('vs')}___{nhl.ico.get('time')}_EST_|_MSK_|_KHV_</code>\n"
                txt += header_scheduled

        # Live
        elif game.get('gameState') in nhl.gameState.get('live'):
            if (header_live == ''):
                header_live = f"\n{nhl.ico.get('live')} <b>Live:</b>\n"
                txt += header_live

        # Final
        elif game.get('gameState') in nhl.gameState.get('final'):
            if (header_finished == ''):
                header_finished = f"\n{nhl.ico.get('finished')} <b>Finished:</b>\n"
                txt += header_finished

        txt += get_schedule_game_text(game, hideScore=hideScore) + "\n"

    return txt


# Формирование теста для вывода сведений об игре
def get_schedule_game_text(game, hideScore=False, inlinemenu=False):

    # Scheduled
    if game.get('gameState') in nhl.gameState.get('scheduled'):
        txt = f"{game.get('awayTeam').get('abbrev')}{nhl.ico.get('vs')}{game.get('homeTeam').get('abbrev')}" \
              f"{nhl.ico.get('time')}{get_game_time_tz_text(game.get('startTimeUTC'), inlinemenu=inlinemenu)}"
        txt = txt if (inlinemenu) else f"<code>{txt}</code>"

    # Live
    elif game.get('gameState') in nhl.gameState.get('live'):
        currentPeriod = game.get('periodDescriptor').get('periodType') if game.get('periodDescriptor').get('number') > 3 else nhl.gamePeriods[game.get('periodDescriptor').get('number')]
        teams_score_text = get_game_teams_score_text(game, hideScore=hideScore, inlinemenu=inlinemenu)
        txt = f"{teams_score_text} - {nhl.ico.get('live')} {currentPeriod}"
        if game.get('clock'):
            txt += f"/{'END' if (game.get('clock').get('inIntermission')) else game.get('clock').get('timeRemaining')}"

    # Final
    elif game.get('gameState') in nhl.gameState.get('final'):
        teams_score_text = get_game_teams_score_text(game, hideScore=hideScore, inlinemenu=inlinemenu)
        txt = f"{teams_score_text} - " \
              f"{nhl.ico.get('finished')} {'' if game.get('periodDescriptor').get('number') == 3 else game.get('periodDescriptor').get('periodType')}"

    # TBD/Postponed
    elif game.get('gameState') in nhl.gameState.get('tbd'):  # 8 - Scheduled (Time TBD); 9 - Postponed
        txt = f"{game.get('awayTeam').get('abbrev')}{nhl.ico.get('vs')}{game.get('homeTeam').get('abbrev')}" \
              f"{nhl.ico.get('tbd')} {game.get('gameState')}"
        txt = txt if (inlinemenu) else f"<code>{txt}</code>"

    # Other
    else:
        txt = f"{game.get('awayTeam').get('abbrev')}{nhl.ico.get('vs')}{game.get('homeTeam').get('abbrev')}"
        txt = txt if (inlinemenu) else f"<code>{txt}</code>"

    return txt


def get_game_teams_score_text(game, hideScore=False, inlinemenu=False):

    away_team = game.get('awayTeam').get('abbrev') if (inlinemenu) else f"<code>{game.get('awayTeam').get('abbrev')}</code>"
    away_team_score = game.get('awayTeam').get('score')

    home_team = game.get('homeTeam').get('abbrev') if (inlinemenu) else f"<code>{game.get('homeTeam').get('abbrev')}</code>"
    home_team_score = game.get('homeTeam').get('score')

    game_teams_score = f"{away_team} {get_game_team_score_text(away_team_score, hideScore=hideScore)}{nhl.ico.get('vs')}{get_game_team_score_text(home_team_score, hideScore=hideScore)} {home_team}"

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

    dtEST = dt.astimezone(nhl.tz.get('EST'))
    dtMSK = dt.astimezone(nhl.tz.get('MSK'))
    dtKHV = dt.astimezone(nhl.tz.get('KHV'))

    str = f"{dtEST.date().isoformat()} {nhl.ico.get('time')} " if (withDate) else ''

    ft = "%H:%M %Z" if (withTZ or inlinemenu) else "%H:%M"
    str += f"{dtEST.strftime(ft)}|{dtMSK.strftime(ft)}|{dtKHV.strftime(ft).replace('+10', 'KHV')}".upper() #lower()

    str = str if (inlinemenu) else f"<code>{str}</code>"

    return str


# Получение корректной даты, если получены пустые данные
def get_correct_date_from_data(data, as_str=True):
    if (data.get('totalItems') > 0):
        day = data.get('dates').get(0).get('date') if (as_str) else date.fromisoformat(data.get('dates').get(0).get('date'))
    else:
        day = datetime.strptime(data.get('metaData').get('timeStamp'), "%Y%m%d_%H%M%S").replace(tzinfo=timezone.utc).astimezone(nhl.tz.get('EST'))
        day = day.date().isoformat() if (as_str) else day

    return day

def get_schedule_data_by_dame_for_leagueRecords(game_id: str):
    schedule_str = f"/schedule?expand=schedule.leagueRecord,schedule.game.seriesSummary&gamePk={game_id}"

    data = nhl.get_request_nhl_api(schedule_str)

    return data

