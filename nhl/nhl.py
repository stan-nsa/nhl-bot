# Меню команд бота
#scores - Результаты текущих матчей
#schedule - Расписание матчей
#standings - Турнирная таблица
#stats - Статистика игроков
#stats_teams - Статистика команд
#teams - Информация по командам


# NHL API Documentation:
# https://github.com/Zmalski/NHL-API-Reference

# Scores: https://api-web.nhle.com/v1/score/now
#         https://api-web.nhle.com/v1/score/2023-11-10

# Season (current):  https://statsapi.web.nhl.com/api/v1/seasons/current
# https://api.nhle.com/stats/rest/en/season?sort=[{"property":"id","direction":"DESC"}]&limit=1

# ESPN News
# http://site.api.espn.com/apis/site/v2/sports/hockey/nhl/news?limit=15

# https://api.nhle.com/stats/rest/en/componentSeason - (возможно, можно будет использовать для определения стадии сезона: предсезонка, регулярка, ПО)


import requests
from emoji import emojize #Overview of all emoji: https://carpedm20.github.io/emoji/   https://k3a.me/telegram-emoji-list-codes-descriptions/
import pytz
from nhl import stats

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
    'report': emojize(':receipt:'),
    'link': emojize(':link:'),
    'point': emojize(':backhand_index_pointing_right:'),

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

# gameState
gameState = {
    'scheduled': {'FUT', 'PRE'},
    'live': {'LIVE', 'CRIT'},
    'final': {'FINAL', 'OFF'},
    'tbd': {'TBD', 'PST'} # 8 - Scheduled (Time TBD); 9 - Postponed
}

# gamePeriods
gamePeriods = {
    1: '1st',
    2: '2nd',
    3: '3rd',
    4: 'OT'
}

# goalType
goalType = {
    'ev': '',       # в равных составах
    'pp': 'PPG',    # в большинстве
    'sh': 'SHG'     # в меньшинстве
}

hide_score = True # Скрывать счёт в командах scores, schedule (в детальных статусах матчей игнорируется)


# Запрос к серверу для получения данных
def get_request_nhl_api(query_str):
    response = requests.get(NHL_API_URL + query_str, params={"Content-Type": "application/json"})#, proxies=proxies)
    return response.json()


# Получение от сервера данных о текущем сезоне
def get_season_current():
    query_str = 'season?sort=[{"property":"id","direction":"DESC"}]&limit=1'

    data = stats.get_request_nhl_stats_api(query_str)

    return data['data'][0]


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
def get_standings_data():
    standings_str = "standings/now"

    data = get_request_nhl_api(standings_str)

    return data['standings']


# Формирование теста для вывода турнирной таблицы в зависимости от типа
def get_standings_text(standingsType=None, full=False):
    data = get_standings_data()

    match standingsType:
        case 'League':
            txt = get_standings_league_text(data, full)

        case 'WildCard':
            txt = get_standings_wildcard_text(data, full)

        case 'Division':
            txt = get_standings_division_text(data, full)

        case _:
            txt = get_standings_division_text(data, full)

    return txt


# Формирование теста для вывода турнирной таблицы с разбивкой по дивизионам
def get_standings_division_text(data, full=False):

    divisions = {'Atlantic': [],
                 'Metropolitan': [],
                 'Central': [],
                 'Pacific': []}

    for team in data:
        divisions[team['divisionName']].append(team)

    for d in divisions.values():
        d = sorted(d, key=lambda d: d['divisionSequence'])

    txt = "<pre>"
    for div_name, div in divisions.items():
        txt += get_standings_table_header_text(caption=div_name, full=full)

        for team in div:
            txt += get_standings_table_row_text(row=team, rank=team['divisionSequence'], full=full)

    return txt + "</pre>"


# Формирование теста для вывода турнирной таблицы с разбивкой по дивизионам с Wild Card
def get_standings_wildcard_text(data, full=False):

    conferences = {'Eastern': {'Atlantic': [], 'Metropolitan': [], 'WildCard': []},
                   'Western': {'Central': [], 'Pacific': [], 'WildCard': []}}

    for team in data:
        if (team['wildcardSequence']):
            conferences[team['conferenceName']]['WildCard'].append(team)
        else:
            conferences[team['conferenceName']][team['divisionName']].append(team)

    for c in conferences.values():
        for name, d in c.items():
            if (name == 'WildCard'):
                d = sorted(d, key=lambda d: d['wildcardSequence'])
            else:
                d = sorted(d, key=lambda d: d['divisionSequence'])

    txt = ""
    for conf_name, conf in conferences.items():
        txt += f"\n<b>{conf_name}</b>\n"
        txt += "<pre>"

        for div_name, div in conf.items():
            txt += get_standings_table_header_text(caption=div_name, full=full)

            for team in div:
                n = team['wildcardSequence'] if (div_name == 'WildCard') else team['divisionSequence']

                txt += get_standings_table_row_text(row=team, rank=n, full=full)

        txt += "</pre>"

    return txt


# Формирование теста для вывода общей турнирной таблицы
def get_standings_league_text(data, full=False):

    txt = "<pre>"

    txt += get_standings_table_header_text(caption='NHL', full=full)

    for team in data:
        txt += get_standings_table_row_text(row=team, rank=team['leagueSequence'], full=full)

    return txt + "</pre>"


# Формирование теста для вывода заголовка турнирной таблицы
def get_standings_table_header_text(caption, full=False):

    txt = ""

    if (full):
        txt += f"\n #|{caption.center(22, '_')}|GP|W_|L_|OT|Pts\n"
    else:
        txt += f"\n #|{caption.center(22, '_')}|GP|Pts\n"

    return txt


# Формирование теста для вывода строки турнирной таблицы
def get_standings_table_row_text(row, rank, full=False):

    in_po_symbol = '*'
    #in_po_symbol = emojize(':star:')

    txt = ""

    in_po = in_po_symbol if (row['wildcardSequence'] < 3) else (' ')

    if (full):
        txt += f"{str(rank).rjust(2)}|" \
               f"{row['teamName']['default'].ljust(21)}{in_po}|" \
               f"{str(row['gamesPlayed']).rjust(2)}|" \
               f"{str(row['wins']).rjust(2)}|" \
               f"{str(row['losses']).rjust(2)}|" \
               f"{str(row['otLosses']).rjust(2)}|" \
               f"{str(row['points']).rjust(3)}\n"
    else:
        txt += f"{str(rank).rjust(2)}|" \
               f"{row['teamName']['default'].ljust(21)}{in_po}|" \
               f"{str(row['gamesPlayed']).rjust(2)}|" \
               f"{str(row['points']).rjust(3)}\n"

    return txt


# Краткое ФИО (И.Фамилия)
def short_player_name(full_name):
    name_parts = full_name.split()
    name = ' '.join([(name_parts[0][:1] + '.'), *name_parts[1:]])

    return name

