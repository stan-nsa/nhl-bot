#https://api.nhle.com/stats/rest/en/goalie/summary?isAggregate=false&isGame=false&sort=[{"property":"wins","direction":"DESC"},{"property":"savePct","direction":"DESC"}]&start=0&limit=50&factCayenneExp=gamesPlayed>=1&cayenneExp=gameTypeId=2 and seasonId=20222023
#https://api.nhle.com/stats/rest/en/goalie/summary?isAggregate=false&isGame=false&sort=[{"property":"savePct","direction":"DESC"}]&start=0&limit=10&factCayenneExp=gamesPlayed>=15&cayenneExp=gameTypeId=2 and seasonId=20222023
# desired stats: S/C(Shoots/Catches), GP, GS, W, L, OT (Overtime Losses), SA (Shots Against), Svs (Saves), GA (Goals Against), Sv% (Save %) GAA (Goals-Against-Avg), TOI, PIM


import requests

from nhl import nhl

NHL_STATS_API_URL = "https://api.nhle.com/stats/rest/en"


# Запрос к серверу для получения данных
def get_request_nhl_stats_api(query_str : str):
    response = requests.get(NHL_STATS_API_URL + query_str, params={"Content-Type": "application/json"})
    return response.json()


def get_stats_goalie(property : str, direction='DESC', limit=10):
    gamesPlayed = 15
    gameTypeId = 2 # 2 = regular season, 3 = playoffs
    seasonId = nhl.get_season_current()['seasonId']

    query_str = '/goalie/summary?isAggregate=false&isGame=false'
    query_str_sort = '&sort=[{"property":"' + property + '","direction":"' + direction + '"}]'
    query_str_limit = f'&start=0&limit={limit}'
    query_str_exp = f'&factCayenneExp=gamesPlayed>={gamesPlayed}&cayenneExp=gameTypeId={gameTypeId} and seasonId={seasonId}'

    query_str += query_str_sort + query_str_limit + query_str_exp

    data = get_request_nhl_stats_api(query_str)

    return data


# Формирование теста для вывода турнирной таблицы с разбивкой по дивизионам
def get_stats_goalie_text(full=False):
    #full = True
    data = get_stats_goalie(property='savePct')

    txt = "<pre>"

    if (full):
        txt += f"\n #|{'Player'.center(21, '_')}|Sv%\n"
    else:
        txt += f"\n #|{'Player'.center(21, '_')}|Sv%\n"

    n = 0
    for player in data['data']:
        n += 1
        if (full):
            #txt += f"{str(n).rjust(2, ' ')}|{player['goalieFullName'].ljust(20, ' ')}({player['teamAbbrevs']})|{round(player['savePct'], 3)}\n"
            txt += f"{str(n).rjust(2, ' ')}|{player['goalieFullName'].ljust(21, ' ')}|{round(player['savePct'], 3)}\n"
        else:
            # txt += f"{str(n).rjust(2, ' ')}|{player['goalieFullName'].ljust(20, ' ')}({player['teamAbbrevs']})|{round(player['savePct'], 3)}\n"
            txt += f"{str(n).rjust(2, ' ')}|{player['goalieFullName'].ljust(21, ' ')}|{round(player['savePct'], 3)}\n"

    return txt + "</pre>"

