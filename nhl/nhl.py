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

# Season (current):
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

    return data.get('data')[0]


# Получение от сервера данных о командах
def get_teams():

    data = get_standings_data()
    teams = sorted(data, key=lambda t: t.get('teamName').get('default'))

    return teams


# Формирование текста информации о команде
def get_team_info(teamAbbrev_teamName):
    teamAbbrev, teamName = teamAbbrev_teamName.split(':')

    txt = f"<b>{teamName}</b>\n"

    teams = get_standings_data()
    team = list(filter(lambda t: t.get('teamAbbrev').get('default') == teamAbbrev, teams))[0]

    # Rank
    txt += "\n<b>Rank:</b>\n"
    n = 10
    txt += "<code>"
    txt += "Division".ljust(n) + f" | #{team.get('divisionSequence')}\n"
    txt += "Conference".ljust(n) + f" | #{team.get('conferenceSequence')}\n"
    txt += "League".ljust(n) + f" | #{team.get('leagueSequence')}\n"
    txt += "WildCard".ljust(n) + f" | {'#' + str(team.get('wildcardSequence')) if team.get('wildcardSequence') else ''}\n"
    txt += "</code>"

    # Stats
    # PP
    pp_data = stats.get_stats_teams_data_byProperty(property='powerPlayPct').get('data')
    t = list(filter(lambda x: x[1].get('teamFullName') == team.get('teamName').get('default'), enumerate(pp_data, 1)))[0]
    pp = round(t[1].get('powerPlayPct') * 100, 1)
    pp_rank = t[0]
    # PK
    pk_data = sorted(pp_data, key=lambda t: t.get('penaltyKillPct'), reverse=True)
    t = list(filter(lambda x: x[1].get('teamFullName') == team.get('teamName').get('default'), enumerate(pk_data, 1)))[0]
    pk = round(t[1].get('penaltyKillPct') * 100, 1)
    pk_rank = t[0]

    txt += "\n<b>Team Stats:</b>\n"
    n = 12
    txt += "<code>"
    txt += "Points".ljust(n) + f" | {team.get('points')}\n"
    txt += "Games Played".ljust(n) + f" | {team.get('gamesPlayed')}\n"
    txt += "W-L-OT".ljust(n) + f" | {team.get('wins')}-{team.get('losses')}-{team.get('otLosses')}\n"
    txt += "home".rjust(n) + f" | {team.get('homeWins')}-{team.get('homeLosses')}-{team.get('homeOtLosses')}\n"
    txt += "away".rjust(n) + f" | {team.get('roadWins')}-{team.get('roadLosses')}-{team.get('roadOtLosses')}\n"
    txt += "last10".rjust(n) + f" | {team.get('l10Wins')}-{team.get('l10Losses')}-{team.get('l10OtLosses')}\n"
    txt += "Streak".ljust(n) + f" | {team.get('streakCode') + str(team.get('streakCount'))}\n"
    txt += "GoalsFor".ljust(n) + f" | {team.get('goalFor')}\n"
    txt += "GoalsAgainst".ljust(n) + f" | {team.get('goalAgainst')}\n"
    txt += "PP%".ljust(n) + f" | {pp} (#{pp_rank})\n"
    txt += "PK%".ljust(n) + f" | {pk} (#{pk_rank})\n"
    txt += "</code>\n"

    txt += get_team_stats_players(teamAbbrev_teamName)

    return txt


def get_team_stats_players_data(teamAbbrev):
    stats_str = f"club-stats/{teamAbbrev}/now"

    data = get_request_nhl_api(stats_str)

    return data


def get_team_stats_players(teamAbbrev_teamName):
    teamAbbrev, teamName = teamAbbrev_teamName.split(':')

    width_player_name = 17  # Ширина поля имени игрока

    txt = f"<b>{teamName}</b>\n"

    data = get_team_stats_players_data(teamAbbrev)
    skaters = sorted(data.get('skaters'), key=lambda s: s.get('points'), reverse=True)

    txt += "<pre>"
    txt += f"_#|{'Skaters'.center(width_player_name, '_').upper()}|Pos|GP|G |A |Pts|+- |PM\n"  # Шапка таблицы статистики полевых
    player_number = 0
    for player in skaters:
        player_number += 1
        player_name = player.get('lastName').get('default')
        player_name = player_name if (len(player_name) <= width_player_name) else f"{player_name[:width_player_name - 3]}..."

        txt += f"{str(player_number).rjust(2)}|" \
               f"{player_name.ljust(width_player_name)}|"

        player_pos = player.get('positionCode')
        player_gp = player.get('gamesPlayed')
        player_goals = player.get('goals')
        player_assists = player.get('assists')
        player_pts = player.get('points')
        player_p_m = f"{'+' if (player.get('plusMinus') > 0) else ''}{player.get('plusMinus')}"
        player_pim = player.get('penaltyMinutes')

        txt += f" {player_pos} |" \
               f"{str(player_gp).rjust(2)}|" \
               f"{str(player_goals).rjust(2)}|" \
               f"{str(player_assists).rjust(2)}|" \
               f"{str(player_pts).rjust(3)}|" \
               f"{player_p_m.rjust(3)}|" \
               f"{str(player_pim).rjust(2)}\n"

    txt += "</pre>"

    return txt


# Получение от сервера данных турнирной таблицы
def get_standings_data():
    standings_str = "standings/now"

    data = get_request_nhl_api(standings_str)

    return data.get('standings')


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
        divisions[team.get('divisionName')].append(team)

    for d in divisions.values():
        d = sorted(d, key=lambda d: d.get('divisionSequence'))

    txt = "<pre>"
    for div_name, div in divisions.items():
        txt += get_standings_table_header_text(caption=div_name, full=full)

        for team in div:
            txt += get_standings_table_row_text(row=team, rank=team.get('divisionSequence'), full=full)

    return txt + "</pre>"


# Формирование теста для вывода турнирной таблицы с разбивкой по дивизионам с Wild Card
def get_standings_wildcard_text(data, full=False):

    conferences = {'Eastern': {'Atlantic': [], 'Metropolitan': [], 'WildCard': []},
                   'Western': {'Central': [], 'Pacific': [], 'WildCard': []}}

    for team in data:
        if (team.get('wildcardSequence')):
            conferences.get(team.get('conferenceName')).get('WildCard').append(team)
        else:
            conferences.get(team.get('conferenceName')).get(team.get('divisionName')).append(team)

    for c in conferences.values():
        for name, d in c.items():
            if (name == 'WildCard'):
                d = sorted(d, key=lambda d: d.get('wildcardSequence'))
            else:
                d = sorted(d, key=lambda d: d.get('divisionSequence'))

    txt = ""
    for conf_name, conf in conferences.items():
        txt += f"\n<b>{conf_name}</b>\n"
        txt += "<pre>"

        for div_name, div in conf.items():
            txt += get_standings_table_header_text(caption=div_name, full=full)

            for team in div:
                n = team.get('wildcardSequence') if (div_name == 'WildCard') else team.get('divisionSequence')

                txt += get_standings_table_row_text(row=team, rank=n, full=full)

        txt += "</pre>"

    return txt


# Формирование теста для вывода общей турнирной таблицы
def get_standings_league_text(data, full=False):

    txt = "<pre>"

    txt += get_standings_table_header_text(caption='NHL', full=full)

    for team in data:
        txt += get_standings_table_row_text(row=team, rank=team.get('leagueSequence'), full=full)

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

    in_po = in_po_symbol if (row.get('wildcardSequence') < 3) else (' ')

    if (full):
        txt += f"{str(rank).rjust(2)}|" \
               f"{row.get('teamName').get('default').ljust(21)}{in_po}|" \
               f"{str(row.get('gamesPlayed')).rjust(2)}|" \
               f"{str(row.get('wins')).rjust(2)}|" \
               f"{str(row.get('losses')).rjust(2)}|" \
               f"{str(row.get('otLosses')).rjust(2)}|" \
               f"{str(row.get('points')).rjust(3)}\n"
    else:
        txt += f"{str(rank).rjust(2)}|" \
               f"{row.get('teamName').get('default').ljust(21)}{in_po}|" \
               f"{str(row.get('gamesPlayed')).rjust(2)}|" \
               f"{str(row.get('points')).rjust(3)}\n"

    return txt


# Краткое ФИО (И.Фамилия)
def short_player_name(full_name):
    name_parts = full_name.split()
    name = ' '.join([(name_parts[0][:1] + '.'), *name_parts[1:]])

    return name

