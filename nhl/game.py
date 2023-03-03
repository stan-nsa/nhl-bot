from nhl import nhl
from nhl import schedule


#== Получение от сервера данных о матче ===========================================================

# Получение от сервера данных о матче
def get_game_data(game_id):

    game_str = f"/game/{game_id}/feed/live"

    data = nhl.get_request_nhl_api(game_str)

    return data


# Формирование теста для вывода информации о матче
def get_game_text(game_id, details='scoringPlays'):
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

    #-- Статистика команд на момент матча: (wins-losses-ot) --
    teams_leagueRecords = schedule.get_schedule_data_by_dame_for_leagueRecords(game_id)['dates'][0]['games'][0]['teams']
    team_away_w_l_o = f"({teams_leagueRecords['away']['leagueRecord']['wins']}-{teams_leagueRecords['away']['leagueRecord']['losses']}-{teams_leagueRecords['away']['leagueRecord']['ot']})"
    team_home_w_l_o = f"({teams_leagueRecords['home']['leagueRecord']['wins']}-{teams_leagueRecords['home']['leagueRecord']['losses']}-{teams_leagueRecords['home']['leagueRecord']['ot']})"
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
    txt += f"\n{txt_game_summary}\n"
    txt += f"\n{txt_game_details}\n"

    return txt


# Формирование теста для детального вывода информации по определенному виду событий (scoringPlays, penaltyPlays)
def game_details_text(data, type_details: str):
    txt = ''

    match type_details:
        case 'scoringPlays': # Изменение счёта
            all_plays = data['liveData']['plays']['allPlays']
            list_plays = data['liveData']['plays'][type_details]

            txt += f"{nhl.ico['scores']}{nhl.ico['goal']} <b>Scoring:</b>\n"

            for idx_play in list_plays:
                score = all_plays[idx_play]

                if (score['about']['periodType'] == 'SHOOTOUT'): # Пропускаем шотауты
                    continue

                score_teams = f"{score['about']['goals']['away']}:{score['about']['goals']['home']}"    # Счёт
                score_team = f"{score['team']['triCode']}"  # Забившая команда
                score_time = f"{score['about']['ordinalNum']}/{score['about']['periodTime']}"   # Время изменения счёта (период/м:с)
                score_strength = f"({score['result']['strength']['code']}) " if (score['result']['strength']['code'] != 'EVEN') else '' # Вывод PPG или SHG
                score_players = score['result']['description']

                txt += f"\n<b>{score_teams}</b> ({score_team}) ({score_time}) {nhl.ico['goal']} {score_strength}{score_players}\n"

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
    team_away_name = data['gameData']['teams']['away']['teamName']
    team_home_name = data['gameData']['teams']['home']['teamName']

    team_away_stats = data['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']
    team_home_stats = data['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']

    team_away_stats_pp = f"{int(team_away_stats['powerPlayGoals'])}/{int(team_away_stats['powerPlayOpportunities'])}"
    team_home_stats_pp = f"{int(team_home_stats['powerPlayGoals'])}/{int(team_home_stats['powerPlayOpportunities'])}"

    widht_1st_field = len(team_away_name)

    txt = "<b>Game Summary:</b>\n"
    txt += '<code>'
    txt += f"{team_away_name} |   vs   | {team_home_name}\n" \
           f"{str(team_away_stats['goals']).rjust(widht_1st_field)} | Goals  | {team_home_stats['goals']}\n" \
           f"{str(team_away_stats['shots']).rjust(widht_1st_field)} | Shots  | {team_home_stats['shots']}\n" \
           f"{str(team_away_stats['blocked']).rjust(widht_1st_field)} | Blocks | {team_home_stats['blocked']}\n" \
           f"{str(team_away_stats['hits']).rjust(widht_1st_field)} |  Hits  | {team_home_stats['hits']}\n" \
           f"{str(team_away_stats['pim']).rjust(widht_1st_field)} |  PIM   | {team_home_stats['pim']}\n" \
           f"{team_away_stats_pp.rjust(widht_1st_field)} |  PP    | {team_home_stats_pp}"
    txt += '</code>'

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
        txt += "<code>"
        for players_pos, players in players_by_positions.items():
            if (players_pos == 'Goalies'):
                txt += f"_#|{players_pos.center(width_player_name, '_')}|Sv|S_|_Sv%_|_TOI_\n" # Шапка таблицы статистики вратарей
            else:
                txt += f"_#|{players_pos.center(width_player_name, '_')}|G|A|+-|S_|PM|_TOI_\n" # Шапка таблицы статистики полевых

            for player in players:
                txt += f"{player}\n"

        txt += "</code>"

    return txt

