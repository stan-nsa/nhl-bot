# Schedule:  https://statsapi.web.nhl.com/api/v1/schedule?expand=schedule.teams,schedule.scoringplays,schedule.game.seriesSummary,seriesSummary.series,schedule.linescore
#            https://statsapi.web.nhl.com/api/v1/schedule?date=2022-11-25
# Standings: https://statsapi.web.nhl.com/api/v1/standings
# Boxscore:  https://statsapi.web.nhl.com/api/v1/game/2021021092/boxscore

#https://records.nhl.com/site/api/franchise

# Season (current):  https://statsapi.web.nhl.com/api/v1/seasons/current

# All players: https://records.nhl.com/site/api/player/

# Goalie:
#https://records.nhl.com/site/api/goalie-season-stats?cayenneExp=seasonId=20222023
#https://records.nhl.com/site/api/goalie-season-stats?cayenneExp=seasonId=20222023&sort=wins&direction=DESC
#https://records.nhl.com/site/api/goalie-season-stats?cayenneExp=seasonId=20222023&sort=goalsAgainstAverage&direction=ASC
#https://records.nhl.com/site/api/goalie-season-stats?cayenneExp=seasonId=20222023&sort=gamesPlayed&direction=DESC

#https://api.nhle.com/stats/rest/en/goalie/summary?isAggregate=false&isGame=false&sort=[{"property":"wins","direction":"DESC"},{"property":"savePct","direction":"DESC"}]&start=0&limit=50&factCayenneExp=gamesPlayed>=1&cayenneExp=gameTypeId=2 and seasonId<=20222023 and seasonId>=20222023
# desired stats: S/C(Shoots/Catches), GP, GS, W, L, OT (Overtime Losses), SA (Shots Against), Svs (Saves), GA (Goals Against), Sv% (Save %) GAA (Goals-Against-Avg), TOI, PIM
#https://api.nhle.com/stats/rest/en/goalie/summary?isAggregate=false&isGame=false&sort=[{"property":"wins","direction":"DESC"},{"property":"savePct","direction":"DESC"}]&start=0&limit=50&factCayenneExp=gamesPlayed>=1&cayenneExp=franchiseId=16 and gameTypeId=2 and seasonId<=20222023 and seasonId>=20222023

# Skater:
#https://records.nhl.com/site/api/skater-playoff-scoring?cayenneExp=seasonId=20212022&sort=points&direction=DESC
#https://records.nhl.com/site/api/skater-playoff-scoring?cayenneExp=seasonId=20212022&sort=goals&direction=DESC
#https://records.nhl.com/site/api/skater-playoff-scoring?cayenneExp=seasonId=20212022&sort=gamesPlayed&direction=DESC

#https://api.nhle.com/stats/rest/en/skater/summary?isAggregate=false&isGame=false&sort=[{"property":"points","direction":"DESC"},{"property":"goals","direction":"DESC"},{"property":"assists","direction":"DESC"}]&start=0&limit=50&factCayenneExp=gamesPlayed>=1&cayenneExp=franchiseId%3D32 and gameTypeId=2 and seasonId<=20192020 and seasonId>=20192020
#https://api.nhle.com/stats/rest/en/skater/summary?isAggregate=false&isGame=false&sort=[{"property":"points","direction":"DESC"},{"property":"goals","direction":"DESC"},{"property":"assists","direction":"DESC"}]&start=0&limit=50&factCayenneExp=gamesPlayed>=1&cayenneExp=franchiseId=16 and gameTypeId=2 and seasonId<=20222023 and seasonId>=20222023
#https://api.nhle.com/stats/rest/en/skater/summary?isAggregate=false&isGame=false&sort=[{"property":"points","direction":"DESC"},{"property":"goals","direction":"DESC"},{"property":"assists","direction":"DESC"}]&start=0&limit=50&factCayenneExp=gamesPlayed>=1&cayenneExp=gameTypeId=2 and seasonId<=20222023 and seasonId>=20222023
#Def https://api.nhle.com/stats/rest/en/skater/summary?isAggregate=false&isGame=false&sort=[{"property":"points","direction":"DESC"}]&start=0&limit=50&factCayenneExp=gamesPlayed>=1&cayenneExp=gameTypeId=2 and seasonId<=20222023 and seasonId>=20222023 and positionCode="D"
#Rookie https://api.nhle.com/stats/rest/en/skater/summary?isAggregate=false&isGame=false&sort=[{"property":"points","direction":"DESC"}]&start=0&limit=50&factCayenneExp=gamesPlayed>=1&cayenneExp=gameTypeId=2 and seasonId<=20222023 and seasonId>=20222023 and isRookie=1


#https://api.nhle.com/stats/rest/en/franchise?sort=fullName&include=lastSeason.id&include=firstSeason.id
#https://api.nhle.com/stats/rest/en/shiftcharts?cayenneExp=gameId=

# Player image URLs
#        https://nhl.bamcontent.com/images/headshots/current/168x168/###.jpg";  // Image URL for for player 8471675 (Sidney Crosby): https://nhl.bamcontent.com/images/headshots/current/168x168/8471675@2x.jpg
#        https://nhl.bamcontent.com/images/headshots/current/168x168/###@2x.jpg";  // Image URL for 2x size for player 8471675 (Sidney Crosby): https://nhl.bamcontent.com/images/headshots/current/168x168/8471675@2x.jpg
#        https://nhl.bamcontent.com/images/headshots/current/168x168/###@3x.jpg"; // Image URL for 3x size for player 8471675 (Sidney Crosby): https://nhl.bamcontent.com/images/headshots/current/168x168/8471675@2x.jpg

# ESPN News
#http://site.api.espn.com/apis/site/v2/sports/hockey/nhl/news?limit=15


import requests
#from datetime import datetime, timezone, date, timedelta
#import pytz
#from emoji import emojize #Overview of all emoji: https://carpedm20.github.io/emoji/
#import db

NHL_API_URL = "https://statsapi.web.nhl.com/api/v1"

proxies = {
    'http': 'socks5://puser:8888@rkn-pnh.hopto.org:8888',
    'https': 'socks5://puser:8888@rkn-pnh.hopto.org:8888'
}

proxies = None

# Запрос к серверу для получения данных
def get_request_nhl_api(query_str):
    response = requests.get(NHL_API_URL + query_str, params={"Content-Type": "application/json"}, proxies=proxies)
    return response.json()


# Получение от сервера данных о текущем сезоне
def get_season_current():
    query_str = '/seasons/current'

    data = get_request_nhl_api(query_str)

    return data['seasons'][0]


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
    #full = True
    data = get_standings()

    txt = "<pre>"
    in_po_symbol = '*'
    #in_po_symbol = emojize(':star:')
    for div in data:
        if (full):
            txt += f"\n#|{div['division']['name'].center(22, '_')}|GP|W |L |O |Pt\n"
        else:
            txt += f"\n#|{div['division']['name'].center(22, '_')}|GP|Pt\n"

        for team in div['teamRecords']:
            in_po = in_po_symbol if (int(team['wildCardRank']) < 3) else (' ')
            if (full):
                txt += f"{team['divisionRank']}|{team['team']['name'].ljust(21, ' ')}{in_po}|{team['gamesPlayed']}|{str(team['leagueRecord']['wins']).ljust(2, ' ')}|{str(team['leagueRecord']['losses']).ljust(2, ' ')}|{str(team['leagueRecord']['ot']).ljust(2, ' ')}|{team['points']}\n"
            else:
                txt += f"{team['divisionRank']}|{team['team']['name'].ljust(21, ' ')}{in_po}|{team['gamesPlayed']}|{team['points']}\n"

    return txt + "</pre>"


#print(get_schedule_today())

