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

import requests

from nhl import nhl

NHL_STATS_API_URL = "https://api.nhle.com/stats/rest/en"

goalie_stats = {
    'savePct': 'Sv%',
    'goalsAgainstAverage': 'GGA',
    'shutouts': 'SO',
    'wins': 'W'
}

skater_stats = {
    'points': 'P',
    'goals': 'G',
    'assists': 'A'
}


# Запрос к серверу для получения данных
def get_request_nhl_stats_api(query_str: str):
    response = requests.get(NHL_STATS_API_URL + query_str, params={"Content-Type": "application/json"}, proxies=nhl.proxies)
    return response.json()


#-- Статистика вратарей ---------------------------------------------------------------------------
# Получение данных вратарской статистики по указанному стат.показателю
def get_stats_goalie_data_byProperty(property: str, direction='DESC', limit=10):
    gamesPlayed = 15
    gameTypeId = 2 # 2 = regular season, 3 = playoffs
    seasonId = nhl.get_season_current()['seasonId']

    query_str = '/goalie/summary?isAggregate=false&isGame=false'
    query_str_sort = '&sort=[{"property":"' + property + '","direction":"' + direction + '"}]'
    query_str_limit = f'&start=0&limit={limit}'
    query_str_exp = f'&factCayenneExp=gamesPlayed>={gamesPlayed}&cayenneExp=gameTypeId={gameTypeId} and seasonId={seasonId}'

    query_str += query_str_sort + query_str_limit + query_str_exp

    data = get_request_nhl_stats_api(query_str)

    data['stata'] = property

    return data


# Формирование теста для вывода вратарской статистики
def get_stats_goalie_text_fromData(data, full=False):
    #full = True
    txt = "<pre>"

    if (full):
        txt += f"\n #|{'Goalie'.center(21, '_')}|{goalie_stats[data['stata']]}\n"
    else:
        txt += f"\n #|{'Goalie'.center(21, '_')}|{goalie_stats[data['stata']]}\n"

    n = 0
    for player in data['data']:
        n += 1
        if (full):
            #txt += f"{str(n).rjust(2, ' ')}|{player['goalieFullName'].ljust(20, ' ')}({player['teamAbbrevs']})|{round(player[data['stata']], 3)}\n"
            txt += f"{str(n).rjust(2, ' ')}|{player['goalieFullName'].ljust(21, ' ')}|{round(player[data['stata']], 3)}\n"
        else:
            # txt += f"{str(n).rjust(2, ' ')}|{player['goalieFullName'].ljust(20, ' ')}({player['teamAbbrevs']})|{round(player[data['stata']], 3)}\n"
            txt += f"{str(n).rjust(2, ' ')}|{player['goalieFullName'].ljust(21, ' ')}|{round(player[data['stata']], 3)}\n"

    return txt + "</pre>"


# Формирование теста для вывода вратарской статистики по указанному стат.показателю
def get_stats_goalie_byProperty_text(property: str, direction='DESC', limit=10, full=False):
    data = get_stats_goalie_data_byProperty(property, direction, limit)

    text = get_stats_goalie_text_fromData(data, full)

    return text


# Формирование теста для вывода вратарских статистик
def get_stats_goalie_text(full=False):
    text = get_stats_goalie_byProperty_text(property='goalsAgainstAverage', direction='ASC', full=full)
    text += get_stats_goalie_byProperty_text('savePct', full=full)
    text += get_stats_goalie_byProperty_text('shutouts', full=full)
    #text += get_stats_goalie_byProperty_text('wins', full=full)

    return text


#-- Статистика полевых ----------------------------------------------------------------------------
# Получение данных статистики полевых по указанному стат.показателю
def get_stats_skater_data_byProperty(property: str, direction='DESC', limit=10):
    gamesPlayed = 1
    gameTypeId = 2 # 2 = regular season, 3 = playoffs
    seasonId = nhl.get_season_current()['seasonId']

    query_str = '/skater/summary?isAggregate=false&isGame=false'
    query_str_sort = '&sort=[{"property":"' + property + '","direction":"' + direction + '"}]'
    query_str_limit = f'&start=0&limit={limit}'
    query_str_exp = f'&factCayenneExp=gamesPlayed>={gamesPlayed}&cayenneExp=gameTypeId={gameTypeId} and seasonId={seasonId}'

    query_str += query_str_sort + query_str_limit + query_str_exp

    data = get_request_nhl_stats_api(query_str)

    data['stata'] = property

    return data


# Формирование теста для вывода статистики полевых
def get_stats_skater_text_fromData(data, full=False):
    #full = True
    txt = "<pre>"

    if (full):
        txt += f"\n #|{'Skaters'.center(21, '_')}|{skater_stats[data['stata']]}\n"
    else:
        txt += f"\n #|{'Skaters'.center(21, '_')}|{skater_stats[data['stata']]}\n"

    n = 0
    for player in data['data']:
        n += 1
        if (full):
            #txt += f"{str(n).rjust(2, ' ')}|{player['skaterFullName'].ljust(20, ' ')}({player['teamAbbrevs']})|{round(player[data['stata']], 3)}\n"
            txt += f"{str(n).rjust(2, ' ')}|{player['skaterFullName'].ljust(21, ' ')}|{round(player[data['stata']], 3)}\n"
        else:
            # txt += f"{str(n).rjust(2, ' ')}|{player['skaterFullName'].ljust(20, ' ')}({player['teamAbbrevs']})|{round(player[data['stata']], 3)}\n"
            txt += f"{str(n).rjust(2, ' ')}|{player['skaterFullName'].ljust(21, ' ')}|{round(player[data['stata']], 3)}\n"

    return txt + "</pre>"


# Формирование теста для вывода статистики полевых по указанному стат.показателю
def get_stats_skater_byProperty_text(property: str, direction='DESC', limit=10, full=False):
    data = get_stats_skater_data_byProperty(property, direction, limit)

    text = get_stats_skater_text_fromData(data, full)

    return text


# Формирование теста для вывода статистик полевых
def get_stats_skater_text(full=False):
    text = get_stats_skater_byProperty_text(property='points', full=full)
    text += get_stats_skater_byProperty_text('goals', full=full)
    text += get_stats_skater_byProperty_text('assists', full=full)

    return text


#-- Статистика защитников -------------------------------------------------------------------------
# Получение данных статистики защитников по указанному стат.показателю
def get_stats_defensemen_data_byProperty(property: str, direction='DESC', limit=10):
    gamesPlayed = 1
    gameTypeId = 2 # 2 = regular season, 3 = playoffs
    seasonId = nhl.get_season_current()['seasonId']

    query_str = '/skater/summary?isAggregate=false&isGame=false'
    query_str_sort = '&sort=[{"property":"' + property + '","direction":"' + direction + '"}]'
    query_str_limit = f'&start=0&limit={limit}'
    query_str_exp = f'&factCayenneExp=gamesPlayed>={gamesPlayed}&cayenneExp=positionCode="D" and gameTypeId={gameTypeId} and seasonId={seasonId}'

    query_str += query_str_sort + query_str_limit + query_str_exp

    data = get_request_nhl_stats_api(query_str)

    data['stata'] = property

    return data


# Формирование теста для вывода статистики защитников
def get_stats_defensemen_text_fromData(data, full=False):
    #full = True
    txt = "<pre>"

    if (full):
        txt += f"\n #|{'Defensemens'.center(21, '_')}|{skater_stats[data['stata']]}\n"
    else:
        txt += f"\n #|{'Defensemens'.center(21, '_')}|{skater_stats[data['stata']]}\n"

    n = 0
    for player in data['data']:
        n += 1
        if (full):
            #txt += f"{str(n).rjust(2, ' ')}|{player['skaterFullName'].ljust(20, ' ')}({player['teamAbbrevs']})|{round(player[data['stata']], 3)}\n"
            txt += f"{str(n).rjust(2, ' ')}|{player['skaterFullName'].ljust(21, ' ')}|{round(player[data['stata']], 3)}\n"
        else:
            # txt += f"{str(n).rjust(2, ' ')}|{player['skaterFullName'].ljust(20, ' ')}({player['teamAbbrevs']})|{round(player[data['stata']], 3)}\n"
            txt += f"{str(n).rjust(2, ' ')}|{player['skaterFullName'].ljust(21, ' ')}|{round(player[data['stata']], 3)}\n"

    return txt + "</pre>"


# Формирование теста для вывода статистики защитников по указанному стат.показателю
def get_stats_defensemen_byProperty_text(property: str, direction='DESC', limit=10, full=False):
    data = get_stats_defensemen_data_byProperty(property, direction, limit)

    text = get_stats_defensemen_text_fromData(data, full)

    return text


# Формирование теста для вывода статистик защитников
def get_stats_defensemen_text(full=False):
    text = get_stats_defensemen_byProperty_text(property='points', full=full)
    text += get_stats_defensemen_byProperty_text('goals', full=full)
    text += get_stats_defensemen_byProperty_text('assists', full=full)

    return text


#-- Статистика новичков -------------------------------------------------------------------------
# Получение данных статистики новичков по указанному стат.показателю
def get_stats_rookie_data_byProperty(property: str, direction='DESC', limit=10):
    gamesPlayed = 1
    gameTypeId = 2 # 2 = regular season, 3 = playoffs
    seasonId = nhl.get_season_current()['seasonId']

    query_str = '/skater/summary?isAggregate=false&isGame=false'
    query_str_sort = '&sort=[{"property":"' + property + '","direction":"' + direction + '"}]'
    query_str_limit = f'&start=0&limit={limit}'
    query_str_exp = f'&factCayenneExp=gamesPlayed>={gamesPlayed}&cayenneExp=isRookie=1 and gameTypeId={gameTypeId} and seasonId={seasonId}'

    query_str += query_str_sort + query_str_limit + query_str_exp

    data = get_request_nhl_stats_api(query_str)

    data['stata'] = property

    return data


# Формирование теста для вывода статистики новичков
def get_stats_rookie_text_fromData(data, full=False):
    #full = True
    txt = "<pre>"

    if (full):
        txt += f"\n #|{'Rookies'.center(21, '_')}|{skater_stats[data['stata']]}\n"
    else:
        txt += f"\n #|{'Rookies'.center(21, '_')}|{skater_stats[data['stata']]}\n"

    n = 0
    for player in data['data']:
        n += 1
        if (full):
            #txt += f"{str(n).rjust(2, ' ')}|{player['skaterFullName'].ljust(20, ' ')}({player['teamAbbrevs']})|{round(player[data['stata']], 3)}\n"
            txt += f"{str(n).rjust(2, ' ')}|{player['skaterFullName'].ljust(21, ' ')}|{round(player[data['stata']], 3)}\n"
        else:
            # txt += f"{str(n).rjust(2, ' ')}|{player['skaterFullName'].ljust(20, ' ')}({player['teamAbbrevs']})|{round(player[data['stata']], 3)}\n"
            txt += f"{str(n).rjust(2, ' ')}|{player['skaterFullName'].ljust(21, ' ')}|{round(player[data['stata']], 3)}\n"

    return txt + "</pre>"


# Формирование теста для вывода статистики новичков по указанному стат.показателю
def get_stats_rookie_byProperty_text(property: str, direction='DESC', limit=10, full=False):
    data = get_stats_rookie_data_byProperty(property, direction, limit)

    text = get_stats_rookie_text_fromData(data, full)

    return text


# Формирование теста для вывода статистик новичков
def get_stats_rookie_text(full=False):
    text = get_stats_rookie_byProperty_text(property='points', full=full)
    text += get_stats_rookie_byProperty_text('goals', full=full)
    text += get_stats_rookie_byProperty_text('assists', full=full)

    return text


#-- Общая статистика ------------------------------------------------------------------------------
# Формирование теста для вывода статистик
def get_stats_text(full=False):
    text = get_stats_skater_text(full=full)
    text += get_stats_goalie_text(full=full)
    text += get_stats_defensemen_text(full=full)
    text += get_stats_rookie_text(full=full)

    return text

