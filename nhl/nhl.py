# Меню команд бота
#scores - Результаты текущих матчей
#schedule - Расписание матчей
#standings - Турнирная таблица
#stats - Статистика игроков
#stats_teams - Статистика команд


# Scores: https://api-web.nhle.com/v1/score/now
#         https://api-web.nhle.com/v1/score/2023-11-10

# Season (current):  https://statsapi.web.nhl.com/api/v1/seasons/current
# ESPN News
# http://site.api.espn.com/apis/site/v2/sports/hockey/nhl/news?limit=15


import requests
from emoji import emojize #Overview of all emoji: https://carpedm20.github.io/emoji/   https://k3a.me/telegram-emoji-list-codes-descriptions/
import pytz

# from datetime import datetime, timezone, date, timedelta
# import db

#OLD NHL_API_URL = "https://statsapi.web.nhl.com/api/v1"
NHL_API_URL = "https://api-web.nhle.com/v1/"

proxies = {
    'http': 'socks5://puser:8888@rkn-pnh.hopto.org:8888',
    'https': 'socks5://puser:8888@rkn-pnh.hopto.org:8888'
}

proxies = None

# Иконки/значки для статусов и визуализации информации
ico = {
    'hockey': emojize(':ice_hockey:'),
    'schedule': emojize(':calendar:'),
    'scores': emojize(':goal_net::ice_hockey:'),
    'time': emojize(':alarm_clock:'),
    'standings': emojize(':trophy:'),
    'stats': emojize(':bar_chart:'),

    'scheduled': emojize(':calendar:'),
    'live': emojize(':green_circle:'),
    'finished': emojize(':chequered_flag:'),
    'tbd': emojize(':purple_circle:'),

    'info': emojize(':information:'),
    'prev': emojize(':left_arrow:'),
    'next': emojize(':right_arrow:'),


    'stick': emojize(':ice_hockey:'),
    'vs': emojize(':ice_hockey:'), # Versus
    'skater': emojize(':ice_hockey:'),
    'goalie': emojize(':goal_net:'),
    'goal': emojize(':police_car_light:'),
    'penalty': emojize(':stop_sign:') #:boxing_gloves: :boxing_glove: :stop_sign: :octagonal_sign: :parking:
}

# TimeZone
tz = {
    'EST': pytz.timezone("US/Eastern"),
    'MSK': pytz.timezone("Europe/Moscow"),
    'VLAT': pytz.timezone("Asia/Vladivostok"),
    'KHV': pytz.timezone("Asia/Vladivostok")
}

# gameType
gameType = {
    'regular': {'id': 2, 'name': 'Regular season', 'min_games_played_skaters': 1, 'min_games_played_goalies': 4}, # regular season (min_games_played_goalies = 15)
    'playoff': {'id': 3, 'name': 'PlayOff', 'min_games_played_skaters': 1, 'min_games_played_goalies': 1}  # playoffs
}

hide_score = True # Скрывать счёт в командах scores, schedule (в детальных статусах матчей игнорируется)


# Запрос к серверу для получения данных
def get_request_nhl_api(query_str):
    response = requests.get(NHL_API_URL + query_str, params={"Content-Type": "application/json"})#, proxies=proxies)
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
def get_standings_data(standingsType=None):
    standings_str = "/standings" + (f"/{standingsType}" if (standingsType) else '')

    data = get_request_nhl_api(standings_str)

    return data['records']


# Формирование теста для вывода турнирной таблицы в зависимости от типа
def get_standings_text(standingsType=None, full=False):
    match standingsType:
        case 'byLeague':
            txt = get_standings_league_text(full)

        case 'wildCardWithLeaders':
            txt = get_standings_wildcard_text(full)

        case 'byDivision':
            txt = get_standings_division_text(full)

        case _:
            txt = get_standings_division_text(full)

    return txt


# Формирование теста для вывода турнирной таблицы с разбивкой по дивизионам
def get_standings_division_text(full=False):
    # full = True
    data = get_standings_data()

    txt = "<pre>"
    in_po_symbol = '*'
    # in_po_symbol = emojize(':star:')
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


# Формирование теста для вывода турнирной таблицы с разбивкой по дивизионам с Wild Card
def get_standings_wildcard_text(full=False):
    # full = True
    data = get_standings_data('wildCardWithLeaders')

    conferences = {'Eastern': {'divisions': [*data[2:4]], 'wild': data[0]},
                   'Western': {'divisions': [*data[4:]], 'wild': data[1]}}

    txt = ""
    in_po_symbol = '*'
    # in_po_symbol = emojize(':star:')
    for conf_name, conf in conferences.items():
        txt += f"\n<b>{conf_name}</b>\n"
        txt += "<pre>"

        for div in conf['divisions']:
            if (full):
                txt += f"\n #|{div['division']['name'].center(22, '_')}|GP|W |L |O |Pt\n"
            else:
                txt += f"\n #|{div['division']['name'].center(22, '_')}|GP|Pt\n"

            for team in div['teamRecords']:
                in_po = in_po_symbol if (int(team['wildCardRank']) < 3) else (' ')
                if (full):
                    txt += f"{team['divisionRank'].rjust(2, ' ')}|{team['team']['name'].ljust(21, ' ')}{in_po}|{team['gamesPlayed']}|{str(team['leagueRecord']['wins']).ljust(2, ' ')}|{str(team['leagueRecord']['losses']).ljust(2, ' ')}|{str(team['leagueRecord']['ot']).ljust(2, ' ')}|{team['points']}\n"
                else:
                    txt += f"{team['divisionRank'].rjust(2, ' ')}|{team['team']['name'].ljust(21, ' ')}{in_po}|{team['gamesPlayed']}|{team['points']}\n"

        if (full):
            txt += f"\n #|{'Wild Card'.center(22, '_')}|GP|W |L |O |Pt\n"
        else:
            txt += f"\n #|{'Wild Card'.center(22, '_')}|GP|Pt\n"

        for team in conf['wild']['teamRecords']:
            in_po = in_po_symbol if (int(team['wildCardRank']) < 3) else (' ')
            if (full):
                txt += f"{team['wildCardRank'].rjust(2, ' ')}|{team['team']['name'].ljust(21, ' ')}{in_po}|{team['gamesPlayed']}|{str(team['leagueRecord']['wins']).ljust(2, ' ')}|{str(team['leagueRecord']['losses']).ljust(2, ' ')}|{str(team['leagueRecord']['ot']).ljust(2, ' ')}|{team['points']}\n"
            else:
                txt += f"{team['wildCardRank'].rjust(2, ' ')}|{team['team']['name'].ljust(21, ' ')}{in_po}|{team['gamesPlayed']}|{team['points']}\n"

        txt += "</pre>"

    return txt


# Формирование теста для вывода общей турнирной таблицы
def get_standings_league_text(full=False):
    # full = True
    data = get_standings_data('byLeague')

    txt = "<pre>"
    in_po_symbol = '*'
    # in_po_symbol = emojize(':star:')

    if (full):
        txt += f"\n #|{'NHL'.center(22, '_')}|GP|W |L |O |Pt\n"
    else:
        txt += f"\n #|{'NHL'.center(22, '_')}|GP|Pt\n"

    for team in data[0]['teamRecords']:
        in_po = in_po_symbol if (int(team['wildCardRank']) < 3) else (' ')
        if (full):
            txt += f"{team['leagueRank'].rjust(2, ' ')}|{team['team']['name'].ljust(21, ' ')}{in_po}|{team['gamesPlayed']}|{str(team['leagueRecord']['wins']).ljust(2, ' ')}|{str(team['leagueRecord']['losses']).ljust(2, ' ')}|{str(team['leagueRecord']['ot']).ljust(2, ' ')}|{team['points']}\n"
        else:
            txt += f"{team['leagueRank'].rjust(2, ' ')}|{team['team']['name'].ljust(21, ' ')}{in_po}|{team['gamesPlayed']}|{team['points']}\n"

    return txt + "</pre>"


# Краткое ФИО (И.Фамилия)
def short_player_name(full_name):
    name_parts = full_name.split()
    name = ' '.join([(name_parts[0][:1] + '.'), *name_parts[1:]])

    return name

