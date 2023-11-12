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
        txt_game_summary = game_summary_text(boxscore)
        txt_game_details = f"{game_details_text(landing, details)}"

    # Final
    elif boxscore['gameState'] in nhl.gameState['final']:
        txt_game_status = f"{nhl.ico['finished']} <b>Finished:</b> {'' if boxscore['period'] == 3 else boxscore['periodDescriptor']['periodType']}"
        txt_team_away_score = schedule.get_game_team_score_text(boxscore['awayTeam']['score'])
        txt_team_home_score = schedule.get_game_team_score_text(boxscore['homeTeam']['score'])
        txt_game_summary = game_summary_text(boxscore)
        txt_game_details = f"{game_details_text(landing, details)}"

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

def get_game_text_OLD(game_id, details='scoring'):
    data = get_game_data(game_id)

    game = data['gameData']
    live = data['liveData']
    linescore = live['linescore']

    txt_game_status = ''
    txt_game_summary = ''
    txt_game_details = ''
    txt_team_away_score = ''
    txt_team_home_score = ''

    team_away = game['teams']['away']['name']
    team_home = game['teams']['home']['name']
    team_away_score = live['linescore']['teams']['away']['goals']
    team_home_score = live['linescore']['teams']['home']['goals']

    schedule_expand_data = schedule.get_schedule_data_by_dame_for_leagueRecords(game_id)

    #-- Статистика команд на момент матча: (wins-losses-ot) --
    teams_leagueRecords = schedule_expand_data['dates'][0]['games'][0]['teams']
    team_away_w_l_o = f"({teams_leagueRecords['away']['leagueRecord']['wins']}-{teams_leagueRecords['away']['leagueRecord']['losses']}" + \
                      (f"-{teams_leagueRecords['away']['leagueRecord']['ot']})" if (game['game']['type'] == "R") else f")")
    team_home_w_l_o = f"({teams_leagueRecords['home']['leagueRecord']['wins']}-{teams_leagueRecords['home']['leagueRecord']['losses']}" + \
                      (f"-{teams_leagueRecords['home']['leagueRecord']['ot']})" if (game['game']['type'] == "R") else f")")

    # -- Информация о текущей серии ПО (Game #, Team lead) --
    series_summary = f"({schedule_expand_data['dates'][0]['games'][0]['seriesSummary']['gameLabel']}, " \
                     f"{schedule_expand_data['dates'][0]['games'][0]['seriesSummary']['seriesStatus']})\n" if (game['game']['type'] == "P") else ""
    # --------------------------------------------------------

    # Scheduled
    if int(game['status']['statusCode']) < 3:  # 1 - Scheduled; 2 - Pre-Game
        txt_game_status = f"{nhl.ico['time']} <b>Scheduled:</b> {nhl.ico['time']}{schedule.get_game_time_tz_text(game['datetime']['dateTime'], withTZ=True)}"
    # Live
    elif int(game['status']['statusCode']) < 5:  # 3 - Live/In Progress; 4 - Live/In Progress - Critical
        txt_game_status = f"{nhl.ico['live']} <b>Live: {linescore['currentPeriodOrdinal']} / {linescore['currentPeriodTimeRemaining']}</b>"
        txt_team_away_score = schedule.get_game_team_score_text(team_away_score)
        txt_team_home_score = schedule.get_game_team_score_text(team_home_score)
        txt_game_summary = game_summary_text(data)
        txt_game_details = f"{game_details_text(data, details)}"

    # Final
    elif int(game['status']['statusCode']) < 8:  # 5 - Final/Game Over; 6 - Final; 7 - Final
        txt_game_status = f"{nhl.ico['finished']} <b>Finished:</b> {'' if linescore['currentPeriod'] == 3 else linescore['currentPeriodOrdinal']}"
        txt_team_away_score = schedule.get_game_team_score_text(team_away_score)
        txt_team_home_score = schedule.get_game_team_score_text(team_home_score)
        txt_game_summary = game_summary_text(data)
        txt_game_details = f"{game_details_text(data, details)}"

    # TBD/Postponed
    elif int(game['status']['statusCode']) < 10:  # 8 - Scheduled (Time TBD); 9 - Postponed
        txt_game_status = f"{nhl.ico['tbd']} <b>{game['status']['detailedState']}</b>"
    # Other
    else:
        txt_game_status = ""

    #-- Формирование текста вывода информации о матче -----
    txt = f"{nhl.ico['schedule']} <b>{schedule.get_game_time_tz_text(game['datetime']['dateTime'], withDate=True, withTZ=True)}:</b>\n"
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
            scoring = data['summary'][type_details]

            txt += f"{nhl.ico['scores']}{nhl.ico['goal']} <b>Scoring:</b>\n"

            for period in scoring:
                period_txt = f"{period['period']['periodDescriptor']['periodType'] if (period['period'] > 3) else nhl.gamePeriods[period['period']]}"
                txt += f"\n<b>{period_txt}{' period' if (period['period'] < 4) else ''}:</b>"

                for goal in period['goals']:
                    score_teams = f"{goal['awayScore']}:{goal['homeScore']}"    # Счёт
                    score_team = f"{goal['teamAbbrev']}"  # Забившая команда
                    #score_time = f"{period_txt}/{goal['timeInPeriod']}"   # Время изменения счёта (период/м:с)
                    score_time = f"{goal['timeInPeriod']}"  # Время изменения счёта (м:с)
                    score_strength = f"({nhl.goalType[goal['strength']]}) " if (goal['strength'] != 'ev') else ''
                    score_player = f"{goal['firstName']} {goal['lastName']} ({goal['goalsToDate']})"

                    score_assists = ''
                    for assist in goal['assists']:
                        score_assists += ', ' if len(score_assists) else ''
                        score_assists += f"{assist['firstName']} {assist['lastName']} ({assist['assistsToDate']})"

                    txt += f"\n<b>{score_teams}</b> ({score_team}) ({score_time}) {nhl.ico['goal']} {score_strength}{score_player}\n"
                    txt += f" assists: {score_assists}\n" if len(score_assists) else ''

        case 'penaltyPlays': # Нарушения
            all_plays = data['liveData']['plays']['allPlays']
            list_plays = data['liveData']['plays'][type_details]

            txt += f"{nhl.ico['penalty']} <b>Penalties:</b>\n"

            for idx_play in list_plays:
                penalty = all_plays[idx_play]

                penalty_time = f"{penalty['about']['ordinalNum']}/{penalty['about']['periodTime']}"  # Время нарушения (период/м:с)
                penalty_team = f"{penalty['team']['triCode']}"  # Команда нарушителя
                penalty_minutes = penalty['result']['penaltyMinutes']  # Срок отбывания нарушения
                penalty_desc = penalty['result']['description']  # Описание нарушения

                txt += f"\n<b>{penalty_time}</b> ({penalty_team}) ({penalty_minutes} min.) {nhl.ico['penalty']} {penalty_desc}\n"

        case 'teamsStats':  # Статистика игроков команд
            txt += f"<b>Team Stats:</b>\n"
            txt += game_teams_stats_text(data)

    return txt


# Формирование теста для вывода итоговой информации о матче
def game_summary_text(data):
    team_away_name = data['awayTeam']['name']['default']
    team_home_name = data['homeTeam']['name']['default']

    widht_1st_field = len(team_away_name)

    txt = "<b>Game Summary:</b>\n"
    #txt += '<code>'
    txt += '<pre>'
    txt += f"{team_away_name} |   vs   | {team_home_name}\n" \
           f"{str(data['awayTeam']['score']).rjust(widht_1st_field)} | Goals  | {data['homeTeam']['score']}\n" \
           f"{str(data['awayTeam']['sog']).rjust(widht_1st_field)} | Shots  | {data['homeTeam']['sog']}\n" \
           f"{str(data['awayTeam']['blocks']).rjust(widht_1st_field)} | Blocks | {data['homeTeam']['blocks']}\n" \
           f"{str(data['awayTeam']['hits']).rjust(widht_1st_field)} |  Hits  | {data['homeTeam']['hits']}\n" \
           f"{str(data['awayTeam']['pim']).rjust(widht_1st_field)} |  PIM   | {data['homeTeam']['pim']}\n" \
           f"{data['awayTeam']['powerPlayConversion'].rjust(widht_1st_field)} |  PP    | {data['homeTeam']['powerPlayConversion']}"
    #txt += '</code>'
    txt += '</pre>'

    return txt

def game_summary_text_OLD(data):
    team_away_name = data['gameData']['teams']['away']['teamName']
    team_home_name = data['gameData']['teams']['home']['teamName']

    team_away_stats = data['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']
    team_home_stats = data['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']

    team_away_stats_pp = f"{int(team_away_stats['powerPlayGoals'])}/{int(team_away_stats['powerPlayOpportunities'])}"
    team_home_stats_pp = f"{int(team_home_stats['powerPlayGoals'])}/{int(team_home_stats['powerPlayOpportunities'])}"

    widht_1st_field = len(team_away_name)

    txt = "<b>Game Summary:</b>\n"
    #txt += '<code>'
    txt += '<pre>'
    txt += f"{team_away_name} |   vs   | {team_home_name}\n" \
           f"{str(team_away_stats['goals']).rjust(widht_1st_field)} | Goals  | {team_home_stats['goals']}\n" \
           f"{str(team_away_stats['shots']).rjust(widht_1st_field)} | Shots  | {team_home_stats['shots']}\n" \
           f"{str(team_away_stats['blocked']).rjust(widht_1st_field)} | Blocks | {team_home_stats['blocked']}\n" \
           f"{str(team_away_stats['hits']).rjust(widht_1st_field)} |  Hits  | {team_home_stats['hits']}\n" \
           f"{str(team_away_stats['pim']).rjust(widht_1st_field)} |  PIM   | {team_home_stats['pim']}\n" \
           f"{team_away_stats_pp.rjust(widht_1st_field)} |  PP    | {team_home_stats_pp}"
    #txt += '</code>'
    txt += '</pre>'

    return txt


# Формирование теста для вывода статистики игроков
def game_teams_stats_text(data):
    all_players = data['gameData']['players']
    teams = data['liveData']['boxscore']['teams']

    width_player_name = 15 # Ширина поля имени игрока

    txt = ''
    for key, team in teams.items():
        team_name = team['team']['name']
        team_players = team['players']
        team_goalies = team['goalies']
        team_skaters = team['skaters']
        team_scratches = team['scratches']

        players_by_positions = {'Forwards': [], 'Defense': [], 'Goalies': []} # Массив строк статистики игроков, разбитый по игровым позициям

        # Формирование текста статистики полевых
        for skater in team_skaters:
            if skater in team_scratches:
                continue

            player_id = f"ID{skater}"
            player_stats = team_players[player_id]['stats']['skaterStats']

            # Данные статистики полевых
            player_number = team_players[player_id]['jerseyNumber']
            player_name = f"{all_players[player_id]['firstName'][0]}.{all_players[player_id]['lastName']}"
            player_name = player_name if (len(player_name) <= width_player_name) else f"{player_name[:width_player_name-3]}..."
            playr_goals = player_stats['goals']
            playr_assists = player_stats['assists']
            playr_p_m = player_stats['plusMinus']
            playr_shots = player_stats['shots']
            playr_pim = player_stats['penaltyMinutes']
            playr_toi = player_stats['timeOnIce']

            # Строка статистики полевых
            player_txt = f"{player_number.rjust(2)}|" \
                         f"{player_name.ljust(width_player_name)}|" \
                         f"{playr_goals}|" \
                         f"{playr_assists}|" \
                         f"{str(playr_p_m).rjust(2)}|" \
                         f"{str(playr_shots).rjust(2)}|" \
                         f"{str(playr_pim).rjust(2)}|" \
                         f"{playr_toi}"

            player_pos_type = 'Defense' if (team_players[player_id]['position']['type']=='Defenseman') else f"{team_players[player_id]['position']['type']}s"
            players_by_positions[player_pos_type].append(player_txt)

        # Формирование текста статистики вратарей
        for goalie in team_goalies:
            if goalie in team_scratches:
                continue

            player_id = f"ID{goalie}"
            player_stats = team_players[player_id]['stats']['goalieStats']

            # Данные статистики вратарей
            player_number = team_players[player_id]['jerseyNumber']
            player_name = f"{all_players[player_id]['firstName'][0]}.{all_players[player_id]['lastName']}"
            player_name = player_name if (len(player_name) <= width_player_name) else f"{player_name[:width_player_name-3]}..."
            playr_saves = player_stats['saves']
            playr_shots = player_stats['shots']
            playr_savePercentage = (player_stats['savePercentage'] if ('savePercentage' in player_stats.keys()) else 0) / 100
            playr_toi = player_stats['timeOnIce']

            # Строка статистики вратарей
            player_txt = f"{player_number.rjust(2)}|" \
                         f"{player_name.ljust(width_player_name)}|" \
                         f"{str(playr_saves).rjust(2)}|" \
                         f"{str(playr_shots).rjust(2)}|" \
                         f"{str(round(playr_savePercentage, 3)).rjust(5)}|" \
                         f"{playr_toi}"

            players_by_positions['Goalies'].append(player_txt)

        # Формирование окончательного текста статистики нападающих, защитников и вратарей
        txt += f"\n<b>{team_name}</b>\n"
        #txt += "<code>"
        txt += "<pre>"
        for players_pos, players in players_by_positions.items():
            if (players_pos == 'Goalies'):
                txt += f"_#|{players_pos.center(width_player_name, '_')}|Sv|S_|_Sv%_|_TOI_\n" # Шапка таблицы статистики вратарей
            else:
                txt += f"_#|{players_pos.center(width_player_name, '_')}|G|A|+-|S_|PM|_TOI_\n" # Шапка таблицы статистики полевых

            for player in players:
                txt += f"{player}\n"

        #txt += "</code>"
        txt += "</pre>"

    return txt

