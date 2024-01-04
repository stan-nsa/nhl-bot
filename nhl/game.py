# https://api-web.nhle.com/v1/gamecenter/2023020206/landing
# https://api-web.nhle.com/v1/gamecenter/2023020204/boxscore

from nhl import nhl
from nhl import schedule
from nhl import stats


#== Получение от сервера данных о матче ===========================================================

# Получение от сервера данных о матче
def get_game_data(game_id):

    data = {'boxscore': {}, 'landing': {}}

    #OLD game_str = f"/game/{game_id}/feed/live"
    game_boxscore_str = f"gamecenter/{game_id}/boxscore"
    game_landing_str = f"gamecenter/{game_id}/landing"

    data['boxscore'] = nhl.get_request_nhl_api(game_boxscore_str)
    data['landing'] = nhl.get_request_nhl_api(game_landing_str)

    return data


# Формирование теста для вывода информации о матче
def get_game_text(game_id, details='scoring'):
    data = get_game_data(game_id)

    boxscore = data['boxscore']
    landing = data['landing']

    txt_game_summary = ''
    txt_game_details = ''
    txt_team_away_score = ''
    txt_team_home_score = ''

    team_away = f"{landing['awayTeam']['placeName']['default']} {boxscore['awayTeam']['name']['default']}"
    team_home = f"{landing['homeTeam']['placeName']['default']} {boxscore['homeTeam']['name']['default']}"

    # -- Статистика команд --
    query_str = f"team/summary?cayenneExp=gameTypeId={boxscore['gameType']} and seasonId={boxscore['season']} and teamId in ({boxscore['awayTeam']['id']},{boxscore['homeTeam']['id']})"
    data_stats = stats.get_request_nhl_stats_api(query_str)
    team_away_stats = data_stats['data'][0] if (data_stats['data'][0]['teamId'] == boxscore['awayTeam']['id']) else data_stats['data'][1]
    team_home_stats = data_stats['data'][1] if (data_stats['data'][1]['teamId'] == boxscore['homeTeam']['id']) else data_stats['data'][0]

    #-- Статистика команд на момент матча: (wins-losses-ot) --
    team_away_w_l_o = f"({team_away_stats['wins']}-{team_away_stats['losses']}" + \
                      (f"-{team_away_stats['otLosses']})" if (boxscore['gameType'] == nhl.gameType['regular']['id']) else f")")
    team_home_w_l_o = f"({team_home_stats['wins']}-{team_home_stats['losses']}" + \
                      (f"-{team_home_stats['otLosses']})" if (boxscore['gameType'] == nhl.gameType['regular']['id']) else f")")

    # -- Информация о текущей серии ПО (Game #, Team lead) --
    series_summary = ""
    if boxscore['gameType'] == nhl.gameType['playoff']['id']:
        query_str = f"club-schedule/{boxscore['awayTeam']['abbrev']}/week/{boxscore['gameDate']}"
        data_series = nhl.get_request_nhl_api(query_str)
        series_status = data_series['games'][0]['seriesStatus']

        if series_status['awayTeamWins'] == series_status['homeTeamWins']:
            series_score = "Tied"
        elif series_status['awayTeamWins'] > series_status['homeTeamWins']:
            series_score = f"{boxscore['awayTeam']['abbrev']}"
        else:
            series_score = f"{boxscore['homeTeam']['abbrev']}"

        series_score += f" {series_status['awayTeamWins']}-{series_status['homeTeamWins']}"

        series_summary = f"({series_status['roundAbbrev']} G{series_status['gameNumberOfSeries']} | {series_score})"
    # --------------------------------------------------------

    # Scheduled
    if boxscore['gameState'] in nhl.gameState['scheduled']:
        txt_game_status = f"{nhl.ico['time']} <b>Scheduled:</b> {nhl.ico['time']}{schedule.get_game_time_tz_text(boxscore['startTimeUTC'], withTZ=True, inlinemenu=True)}"

    # Live
    elif boxscore['gameState'] in nhl.gameState['live']:
        currentPeriod = boxscore['periodDescriptor']['periodType'] if boxscore['period'] > 3 else nhl.gamePeriods[boxscore['periodDescriptor']['number']]
        txt_game_status = f"{nhl.ico['live']} <b>Live: {currentPeriod} / {'END' if (boxscore['clock']['inIntermission']) else boxscore['clock']['timeRemaining']}</b>"
        txt_team_away_score = schedule.get_game_team_score_text(boxscore['awayTeam']['score'])
        txt_team_home_score = schedule.get_game_team_score_text(boxscore['homeTeam']['score'])
        txt_game_summary = game_summary_text(landing)
        txt_game_details = game_details_text(data, details)

    # Final
    elif boxscore['gameState'] in nhl.gameState['final']:
        txt_game_status = f"{nhl.ico['finished']} <b>Finished:</b> {'' if boxscore['period'] == 3 else boxscore['periodDescriptor']['periodType']}"
        txt_team_away_score = schedule.get_game_team_score_text(boxscore['awayTeam']['score'])
        txt_team_home_score = schedule.get_game_team_score_text(boxscore['homeTeam']['score'])
        txt_game_summary = game_summary_text(landing)
        txt_game_details = game_details_text(data, details)

    # TBD/Postponed
    elif boxscore['gameState'] in nhl.gameState['tbd']:
        txt_game_status = f"{nhl.ico['tbd']} <b>{boxscore['gameState']}</b>"

    # Other
    else:
        txt_game_status = ""

    #-- Формирование текста вывода информации о матче -----
    txt = f"{nhl.ico['schedule']} <b>{schedule.get_game_time_tz_text(boxscore['startTimeUTC'], withDate=True, withTZ=True, inlinemenu=True)}:</b>\n"
    txt += f"\n{txt_game_status}\n"
    txt += f"{txt_team_away_score} <b>{team_away}</b> {team_away_w_l_o}\n"
    txt += f"{txt_team_home_score} <b>{team_home}</b> {team_home_w_l_o}\n"
    txt += series_summary
    txt += f"\n{txt_game_summary}\n"
    txt += f"\n{txt_game_details}\n"

    return txt


# Формирование теста для детального вывода информации по определенному виду событий (scoringPlays, penaltyPlays)
def game_details_text(data, type_details: str):
    txt = ''

    match type_details:
        case 'scoring': # Изменение счёта
            scoring = data['landing']['summary'][type_details]

            txt += f"{nhl.ico['scores']}{nhl.ico['goal']} <b>Scoring:</b>\n"

            for period in scoring:
                period_txt = f"{period['periodDescriptor']['periodType'] if (period['period'] > 3) else nhl.gamePeriods[period['period']]}"
                txt += f"\n<b>{period_txt}{' period' if (period['period'] < 4) else ''}:</b>"

                for goal in period['goals']:
                    score_teams = f"{goal['awayScore']}:{goal['homeScore']}"    # Счёт
                    score_team = f"{goal['teamAbbrev']['default']}"  # Забившая команда
                    score_time = f"{goal['timeInPeriod']}"  # Время изменения счёта (м:с)
                    score_strength = f"({nhl.goalType[goal['strength']]}) " if (goal['strength'] != 'ev') else ''
                    score_player = f"{goal['name']['default']}"
                    score_player_goals = f"({goal['goalsToDate']})" if (period['periodDescriptor']['periodType'] != 'SO') else ''

                    score_assists = ''
                    for assist in goal['assists']:
                        score_assists += ', ' if len(score_assists) else ''
                        score_assists += f"{assist['name']['default']} ({assist['assistsToDate']})"

                    txt += f"\n<b>{score_teams}</b> ({score_team}) ({score_time}) {nhl.ico['goal']} {score_strength}{score_player} {score_player_goals}\n"
                    txt += f" assists: {score_assists}\n" if len(score_assists) else ''

        case 'penalties': # Нарушения
            penalties = data['landing']['summary'][type_details]

            txt += f"{nhl.ico['penalty']} <b>Penalties:</b>\n"

            for period in penalties:
                period_txt = f"{period['periodDescriptor']['periodType'] if (period['period'] > 3) else nhl.gamePeriods[period['period']]}"
                txt += f"\n<b>{period_txt}{' period' if (period['period'] < 4) else ''}:</b>"

                for penalty in period['penalties']:
                    penalty_time = penalty['timeInPeriod']  # Время нарушения (период/м:с)
                    penalty_team = penalty['teamAbbrev']  # Команда нарушителя
                    penalty_minutes = penalty['duration']  # Срок отбывания нарушения
                    penalty_desc = penalty['descKey']  # Описание нарушения
                    penalty_player = penalty['committedByPlayer'] if ('committedByPlayer' in penalty) else '' # Оштрафованный игрок

                    txt += f"\n<b>{penalty_time}</b> ({penalty_team}) {nhl.ico['penalty']} {penalty_player}: {penalty_desc} ({penalty_minutes} min.)\n"

        case 'teamGameStats':  # Статистика игроков команд
            txt += f"{nhl.ico['stats']} <b>Team Stats:</b>\n"
            txt += game_teams_stats_text(data['boxscore'])

        case 'gameReports':  # Отчеты
            reports = data['boxscore']['boxscore']['gameReports']
            txt += f"{nhl.ico['report']} <b>Game Reports:</b>\n\n" \
                   f"{nhl.ico['point']} <a href='" + reports['gameSummary'] + "'>Game Summary</a>\n\n" \
                   f"{nhl.ico['point']} <a href='" + reports['eventSummary'] + "'>Event Summary</a>\n\n" \
                   f"{nhl.ico['point']} <a href='" + reports['rosters'] + "'>Club Playing Roster</a>\n\n" \
                   f"{nhl.ico['point']} <a href='" + reports['shotSummary'] + "'>Shot Summary</a>\n\n" \
                   f"{nhl.ico['point']} <a href='" + reports['toiAway'] + f"'>Time On Ice: {data['boxscore']['awayTeam']['name']['default']}</a>\n\n" \
                   f"{nhl.ico['point']} <a href='" + reports['toiHome'] + f"'>Time On Ice: {data['boxscore']['homeTeam']['name']['default']}</a>"

    return txt


# Формирование теста для вывода итоговой информации о матче
def game_summary_text(data):
    team_away_name = data['awayTeam']['name']['default']
    team_home_name = data['homeTeam']['name']['default']

    widht_1st_field = len(team_away_name)
    widht_stats_abbrev_field = 5    # Ширина колонки аббривиатуры статистики

    txt = "<b>Game Summary:</b>\n"
    #txt += '<code>'
    txt += '<pre>'
    txt += f"{team_away_name} | {'vs'.center(widht_stats_abbrev_field)} | {team_home_name}\n" \
           f"{str(data['awayTeam']['score']).rjust(widht_1st_field)} | {'Goals'.center(widht_stats_abbrev_field)} | {data['homeTeam']['score']}\n"

    for stat in data['summary']['teamGameStats']:
        if (stat['category'] in stats.game_stats):
            txt += f"{str(stat['awayValue']).rjust(widht_1st_field)} | {stats.game_stats[stat['category']].center(widht_stats_abbrev_field)} | {stat['homeValue']}\n"

    #txt += '</code>'
    txt += '</pre>'

    return txt


# Формирование теста для вывода статистики игроков
def game_teams_stats_text(data):
    players_stats = data['boxscore']['playerByGameStats']

    width_player_name = 17 # Ширина поля имени игрока

    txt = ''

    for team, players_positions in players_stats.items():

        team_name = data[team]['name']['default']

        txt += f"\n<b>{team_name}</b>\n"
        # txt += "<code>"
        txt += "<pre>"
        for players_pos, players in players_positions.items():
            if (players_pos == 'goalies'):
                txt += f"_#|{players_pos.center(width_player_name, '_').upper()}|Sv/Sh|_Sv%_|_TOI_\n"  # Шапка таблицы статистики вратарей
            else:
                txt += f"_#|{players_pos.center(width_player_name, '_').upper()}|G|A|+-|S_|PM|_TOI_\n"  # Шапка таблицы статистики полевых

            for player in players:
                player_number = str(player['sweaterNumber']).upper()
                player_name = player['name']['default'].replace('. ', '.')
                player_name = player_name if (len(player_name) <= width_player_name) else f"{player_name[:width_player_name-3]}..."
                player_toi = player['toi']

                txt += f"{player_number.rjust(2)}|" \
                       f"{player_name.ljust(width_player_name)}|"

                if (players_pos == 'goalies'): # Строка статистики вратарей
                    player_ssa = player['saveShotsAgainst']
                    player_savePctg = player['savePctg'] if ('savePctg' in player) else ''

                    txt += f"{player_ssa.center(5)}|" \
                           f"{player_savePctg.center(5)}|"

                else: # Строка статистики полевых
                    player_goals = player['goals']
                    player_assists = player['assists']
                    player_p_m = f"{'+' if (player['plusMinus'] > 0) else ''}{player['plusMinus']}"
                    player_shots = player['shots']
                    player_pim = player['pim']

                    txt += f"{player_goals}|" \
                           f"{player_assists}|" \
                           f"{player_p_m.rjust(2)}|" \
                           f"{str(player_shots).rjust(2)}|" \
                           f"{str(player_pim).rjust(2)}|"

                txt += f"{player_toi}\n"

        # txt += "</code>"
        txt += "</pre>"

    return txt
