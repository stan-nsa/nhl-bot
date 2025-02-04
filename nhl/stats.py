# Goalies
#https://api.nhle.com/stats/rest/en/goalie/summary?isAggregate=false&isGame=false&sort=[{"property":"wins","direction":"DESC"},{"property":"savePct","direction":"DESC"}]&start=0&limit=50&factCayenneExp=gamesPlayed>=1&cayenneExp=gameTypeId=2 and seasonId=20222023
#https://api.nhle.com/stats/rest/en/goalie/summary?isAggregate=false&isGame=false&sort=[{"property":"savePct","direction":"DESC"}]&start=0&limit=10&factCayenneExp=gamesPlayed>=15&cayenneExp=gameTypeId=2 and seasonId=20222023
# desired stats: S/C(Shoots/Catches), GP, GS, W, L, OT (Overtime Losses), SA (Shots Against), Svs (Saves), GA (Goals Against), Sv% (Save %) GAA (Goals-Against-Avg), TOI, PIM

# Skaters
#https://api.nhle.com/stats/rest/en/skater/summary?isAggregate=false&isGame=false&sort=[{"property":"points","direction":"DESC"}]&start=0&limit=10&factCayenneExp=gamesPlayed>=1&cayenneExp=gameTypeId=2 and seasonId=20222023
#https://api.nhle.com/stats/rest/en/skater/summary?isAggregate=false&isGame=false&sort=[{"property":"goals","direction":"DESC"}]&start=0&limit=10&factCayenneExp=gamesPlayed>=1&cayenneExp=gameTypeId=2 and seasonId=20222023
#https://api.nhle.com/stats/rest/en/skater/summary?isAggregate=false&isGame=false&sort=[{"property":"assists","direction":"DESC"}]&start=0&limit=10&factCayenneExp=gamesPlayed>=1&cayenneExp=gameTypeId=2 and seasonId=20222023
#Def https://api.nhle.com/stats/rest/en/skater/summary?isAggregate=false&isGame=false&sort=[{"property":"points","direction":"DESC"}]&start=0&limit=50&factCayenneExp=gamesPlayed>=1&cayenneExp=gameTypeId=2 and seasonId<=20222023 and seasonId>=20222023 and positionCode="D"
#Rookie https://api.nhle.com/stats/rest/en/skater/summary?isAggregate=false&isGame=false&sort=[{"property":"points","direction":"DESC"}]&start=0&limit=50&factCayenneExp=gamesPlayed>=1&cayenneExp=gameTypeId=2 and seasonId<=20222023 and seasonId>=20222023 and isRookie=1

# Teams:
# https://api.nhle.com/stats/rest/en/team/summary?isAggregate=false&isGame=false&sort=[{"property":"points","direction":"DESC"}]&start=0&limit=10&cayenneExp=gameTypeId=2 and seasonId=20222023
# https://api.nhle.com/stats/rest/en/team/summary?isAggregate=false&isGame=false&sort=[{"property":"powerPlayPct","direction":"DESC"}]&start=0&limit=10&cayenneExp=gameTypeId=2 and seasonId=20222023
# https://api.nhle.com/stats/rest/en/team/summary?isAggregate=false&isGame=false&sort=[{"property":"penaltyKillPct","direction":"DESC"}]&start=0&limit=10&cayenneExp=gameTypeId=2 and seasonId=20222023
# https://api.nhle.com/stats/rest/en/team/summary?cayenneExp=gameTypeId=2 and seasonId=20232024 and teamId=4

import requests

from nhl import nhl
from create_bot import proxies

NHL_STATS_API_URL = "https://api.nhle.com/stats/rest/en/"

goalie_stats = {
    'savePct': {'desc': 'Sv%', 'decimal': 3},
    'goalsAgainstAverage': {'desc': 'GGA', 'decimal': 2},
    'shutouts': {'desc': 'SO', 'decimal': 0},
    'wins': {'desc': 'W', 'decimal': 0}
}

skater_stats = {
    'points': 'P',
    'goals': 'G',
    'assists': 'A'
}

team_stats = {
    'points': 'Pts',
    'powerPlayPct': 'PP%',
    'penaltyKillPct': 'PK%',
    'wins': 'Win'
}

game_stats = {
    'sog': 'SOG',
    'faceoffPctg': 'FO%',
    'powerPlay': 'PP',
    'pim': 'PIM',
    'hits': 'Hits',
    'blockedShots': 'BLKS'
}

players_type = {
    'skaters': {'caption': 'Skaters', 'exp': ''},
    'goalies': {'caption': 'Goalies', 'exp': ''},
    'defensemen': {'caption': 'Defensemen', 'exp': ' and positionCode="D"'},
    'rookies': {'caption': 'Rookies', 'exp': ' and isRookie=1'},
}


# Запрос к серверу для получения данных
def get_request_nhl_stats_api(query_str: str):
    url = NHL_STATS_API_URL + query_str
    print(url) # For debug
    response = requests.get(url, params={"Content-Type": "application/json"}, proxies=proxies)
    return response.json()


def decimal_value_to_str(value, decimal=0, without_leading_zero=True):
    # Форматированный вывод числа с плав.точкой: f"{numObj:.{digits}f}"
    s = f"{value:.{decimal}f}"

    if without_leading_zero:
        s = s[1:] if (0 < value < 1) else s

    return s


# Получение от сервера идентификатора текущего сезона для статистики
def get_season_id_for_stats() -> dict:
    query_str = 'componentSeason'

    data = get_request_nhl_stats_api(query_str)

    season_id = data['data'][0]['seasonId']

    return season_id


#-- Статистика вратарей ---------------------------------------------------------------------------
# Получение данных вратарской статистики по указанному стат.показателю
def get_stats_goalies_data_byProperty(property: str, direction='DESC', limit=10, gameType='regular'):
    #gameTypeId: 2 = regular season, 3 = playoffs
    gameTypeId = nhl.gameType[gameType]['id']

    season_id = get_season_id_for_stats()
    season_data = nhl.get_season_data(season_id)

    query_str = 'goalie/summary?isAggregate=false&isGame=false'
    query_str_sort = '&sort=[{"property":"' + property + '","direction":"' + direction + '"}]'
    query_str_limit = f'&start=0&limit={limit}'
    query_str_exp = f'&cayenneExp=gameTypeId={gameTypeId} and seasonId={season_id}'

    if gameType == 'regular':
        gamesPlayed = season_data['minimumRegularGamesForGoalieStatsLeaders']
        query_str_exp += f'&factCayenneExp=gamesPlayed>={gamesPlayed}'
    elif gameType == 'playoff':
        timeOnIce = season_data['minimumPlayoffMinutesForGoalieStatsLeaders'] * 60 # В секундах
        query_str_exp += f'&factCayenneExp=timeOnIce>={timeOnIce}'

    query_str += query_str_sort + query_str_limit + query_str_exp

    data = get_request_nhl_stats_api(query_str)

    data['stata'] = property

    return data


# Формирование теста для вывода вратарской статистики
def get_stats_goalies_text_fromData(data):
    name_field_width = 21

    txt = "<pre>"

    txt += f"\n #|{'Goalies'.center(name_field_width, '_')}|{goalie_stats.get(data.get('stata')).get('desc')}\n"

    n = 0
    for player in data.get('data'):
        n += 1
        value = decimal_value_to_str(player.get(data.get('stata')), decimal=goalie_stats.get(data.get('stata')).get('decimal'))
        txt += f"{str(n).rjust(2)}|{player.get('goalieFullName').ljust(name_field_width)}|{value}\n"

    return txt + "</pre>"


# Формирование теста для вывода вратарской статистики по указанному стат.показателю
def get_stats_goalies_byProperty_text(property: str, direction='DESC', limit=10, gameType='regular'):
    data = get_stats_goalies_data_byProperty(property, direction, limit, gameType=gameType)

    text = get_stats_goalies_text_fromData(data)

    return text


#-- Статистика полевых ----------------------------------------------------------------------------
# Получение данных статистики полевых по указанному стат.показателю
def get_stats_skaters_data_byProperty(property: str, direction='DESC', limit=10, gameType='regular', playersType='skaters'):
    #gameTypeId: 2 = regular season, 3 = playoffs
    gameTypeId = nhl.gameType[gameType]['id']

    gamesPlayed = nhl.gameType[gameType]['min_games_played_skaters']
    season_id = get_season_id_for_stats()

    query_str = 'skater/summary?isAggregate=false&isGame=false'
    query_str_sort = '&sort=[{"property":"' + property + '","direction":"' + direction + '"}]'
    query_str_limit = f'&start=0&limit={limit}'
    query_str_exp = f'&factCayenneExp=gamesPlayed>={gamesPlayed}&cayenneExp=gameTypeId={gameTypeId} and seasonId={season_id}{players_type[playersType]["exp"]}'

    query_str += query_str_sort + query_str_limit + query_str_exp

    data = get_request_nhl_stats_api(query_str)

    data['stata'] = property
    data['caption'] = players_type[playersType]['caption']

    return data


# Формирование теста для вывода статистики полевых
def get_stats_skaters_text_fromData(data):
    name_field_width = 21

    txt = "<pre>"

    txt += f"\n #|{data.get('caption').center(name_field_width, '_')}|{skater_stats.get(data.get('stata'))}\n"

    n = 0
    for player in data.get('data'):
        n += 1
        txt += f"{str(n).rjust(2, ' ')}|{player.get('skaterFullName').ljust(name_field_width, ' ')}|{player.get(data.get('stata'))}\n"

    return txt + "</pre>"


# Формирование теста для вывода статистики полевых по указанному стат.показателю
def get_stats_skaters_byProperty_text(property: str, direction='DESC', limit=10, gameType='regular', playersType='skaters'):
    data = get_stats_skaters_data_byProperty(property, direction, limit, gameType=gameType, playersType=playersType)

    text = get_stats_skaters_text_fromData(data)

    return text


#-- Статистика защитников -------------------------------------------------------------------------
# Получение данных статистики защитников по указанному стат.показателю
def get_stats_defensemen_data_byProperty(property: str, direction='DESC', limit=10, gameType='regular'):
    #gameTypeId: 2 = regular season, 3 = playoffs
    gameTypeId = nhl.gameType[gameType]['id']

    gamesPlayed = nhl.gameType[gameType]['min_games_played_skaters']
    season_id = get_season_id_for_stats()

    query_str = 'skater/summary?isAggregate=false&isGame=false'
    query_str_sort = '&sort=[{"property":"' + property + '","direction":"' + direction + '"}]'
    query_str_limit = f'&start=0&limit={limit}'
    query_str_exp = f'&factCayenneExp=gamesPlayed>={gamesPlayed}&cayenneExp=gameTypeId={gameTypeId} and seasonId={season_id} and positionCode="D"'

    query_str += query_str_sort + query_str_limit + query_str_exp

    data = get_request_nhl_stats_api(query_str)

    data['stata'] = property

    return data


# Формирование теста для вывода статистики защитников
def get_stats_defensemen_text_fromData(data):
    name_field_width = 21

    txt = "<pre>"

    txt += f"\n #|{'Defensemen'.center(name_field_width, '_')}|{skater_stats[data['stata']]}\n"

    n = 0
    for player in data['data']:
        n += 1
        txt += f"{str(n).rjust(2, ' ')}|{player['skaterFullName'].ljust(name_field_width, ' ')}|{player[data['stata']]}\n"

    return txt + "</pre>"


# Формирование теста для вывода статистики защитников по указанному стат.показателю
def get_stats_defensemen_byProperty_text(property: str, direction='DESC', limit=10, gameType='regular'):
    data = get_stats_defensemen_data_byProperty(property, direction, limit, gameType=gameType)

    text = get_stats_defensemen_text_fromData(data)

    return text


# Формирование теста для вывода статистик защитников
# def get_stats_defensemen_text():
#     text = get_stats_defensemen_byProperty_text(property='points')
#     text += get_stats_defensemen_byProperty_text('goals')
#     text += get_stats_defensemen_byProperty_text('assists')
#
#     return text


#-- Статистика новичков -------------------------------------------------------------------------
# Получение данных статистики новичков по указанному стат.показателю
def get_stats_rookies_data_byProperty(property: str, direction='DESC', limit=10, gameType='regular'):
    #gameTypeId: 2 = regular season, 3 = playoffs
    gameTypeId = nhl.gameType[gameType]['id']

    gamesPlayed = nhl.gameType[gameType]['min_games_played_skaters']
    season_id = get_season_id_for_stats()

    query_str = 'skater/summary?isAggregate=false&isGame=false'
    query_str_sort = '&sort=[{"property":"' + property + '","direction":"' + direction + '"}]'
    query_str_limit = f'&start=0&limit={limit}'
    query_str_exp = f'&factCayenneExp=gamesPlayed>={gamesPlayed}&cayenneExp=gameTypeId={gameTypeId} and seasonId={season_id} and isRookie=1'

    query_str += query_str_sort + query_str_limit + query_str_exp

    data = get_request_nhl_stats_api(query_str)

    data['stata'] = property

    return data


# Формирование теста для вывода статистики новичков
def get_stats_rookies_text_fromData(data):
    name_field_width = 21

    txt = "<pre>"

    txt += f"\n #|{'Rookies'.center(name_field_width, '_')}|{skater_stats[data['stata']]}\n"

    n = 0
    for player in data['data']:
        n += 1
        txt += f"{str(n).rjust(2, ' ')}|{player['skaterFullName'].ljust(name_field_width, ' ')}|{player[data['stata']]}\n"

    return txt + "</pre>"


# Формирование теста для вывода статистики новичков по указанному стат.показателю
def get_stats_rookies_byProperty_text(property: str, direction='DESC', limit=10, gameType='regular'):
    data = get_stats_rookies_data_byProperty(property, direction, limit, gameType=gameType)

    text = get_stats_rookies_text_fromData(data)

    return text


# Формирование теста для вывода статистик новичков
# def get_stats_rookies_text():
#     text = get_stats_rookies_byProperty_text(property='points')
#     text += get_stats_rookies_byProperty_text('goals')
#     text += get_stats_rookies_byProperty_text('assists')
#
#     return text


#-- Статистика команд -------------------------------------------------------------------------
# Получение данных статистики команд по указанному стат.показателю
def get_stats_teams_data_byProperty(property: str, direction='DESC', gameType='regular', teamFullName=None, season_id=None):
    #gameTypeId: 2 = regular season, 3 = playoffs
    gameTypeId = nhl.gameType[gameType]['id']

    season_id = season_id if season_id else get_season_id_for_stats()

    query_str = 'team/summary?isAggregate=false&isGame=false'
    query_str_sort = '&sort=[{"property":"' + property + '","direction":"' + direction + '"}]'
    query_str_exp = f'&cayenneExp=gameTypeId={gameTypeId} and seasonId={season_id}' + \
                    (f' and teamFullName="{teamFullName}"' if teamFullName else '')

    query_str += query_str_sort + query_str_exp

    data = get_request_nhl_stats_api(query_str)

    data['stata'] = property

    return data


# Формирование теста для вывода статистики команд
def get_stats_teams_text_fromData(data):
    name_field_width = 21
    txt = "<pre>"

    txt += f"\n #|{'Team'.center(name_field_width, '_')}|{team_stats[data['stata']]}\n"

    n = 0
    for team in data['data']:
        n += 1
        value = decimal_value_to_str(team[data['stata']]*100, decimal=1) if (team[data['stata']] < 1) else team[data['stata']]
        txt += f"{str(n).rjust(2, ' ')}|{team['teamFullName'].ljust(name_field_width, ' ')}|{value}\n"

    return txt + "</pre>"


# Формирование теста для вывода статистики команд по указанному стат.показателю
def get_stats_teams_byProperty_text(property: str, direction='DESC', gameType='regular'):
    data = get_stats_teams_data_byProperty(property, direction, gameType=gameType)

    text = get_stats_teams_text_fromData(data)

    return text
