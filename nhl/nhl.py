# Schedule:  https://statsapi.web.nhl.com/api/v1/schedule?expand=schedule.teams,schedule.scoringplays,schedule.game.seriesSummary,seriesSummary.series,schedule.linescore
#            https://statsapi.web.nhl.com/api/v1/schedule?date=2022-11-25
# Standings: https://statsapi.web.nhl.com/api/v1/standings
# Boxscore:  https://statsapi.web.nhl.com/api/v1/game/2021021092/boxscore

# All players: https://records.nhl.com/site/api/player/

# Goalie:
#https://records.nhl.com/site/api/goalie-season-stats?cayenneExp=seasonId=20222023
#https://records.nhl.com/site/api/goalie-season-stats?cayenneExp=seasonId=20222023&sort=wins&direction=DESC
#https://records.nhl.com/site/api/goalie-season-stats?cayenneExp=seasonId=20222023&sort=goalsAgainstAverage&direction=ASC
#https://records.nhl.com/site/api/goalie-season-stats?cayenneExp=seasonId=20222023&sort=gamesPlayed&direction=DESC

# Skater:
#https://records.nhl.com/site/api/skater-playoff-scoring?cayenneExp=seasonId=20212022&sort=points&direction=DESC
#https://records.nhl.com/site/api/skater-playoff-scoring?cayenneExp=seasonId=20212022&sort=goals&direction=DESC
#https://records.nhl.com/site/api/skater-playoff-scoring?cayenneExp=seasonId=20212022&sort=gamesPlayed&direction=DESC


import requests
#from datetime import datetime, timezone, date, timedelta
#import pytz
#from emoji import emojize #Overview of all emoji: https://carpedm20.github.io/emoji/
#import db

NHL_API_URL = "https://statsapi.web.nhl.com/api/v1"


# Запрос к серверу для получения данных
def get_request_nhl_api(query_str):
    response = requests.get(NHL_API_URL + query_str, params={"Content-Type": "application/json"})
    return response.json()


# Получение от сервера данных о командах
def get_teams():
    teams_str = '/teams'

    data = get_request_nhl_api(teams_str)

    return data['teams']


# Формирование текста списка команд
def get_teams_for_settings():
    teams = get_teams()
    txt = ""
    for team in teams:
        txt += f"{team['name']}\n"

    return txt


# Получение от сервера данных турнирной таблицы
def get_standings():
    standings_str = "/standings"

    data = get_request_nhl_api(standings_str)

    return data['records']


# Формирование теста для вывода турнирной таблицы с разбивкой по дивизионам
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


#print(get_schedule_today())

