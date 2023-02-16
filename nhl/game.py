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
        txt_game_details = f"{game_plays_details_text(live['plays'], details)}"

    # Final
    elif int(game['status']['statusCode']) < 8:  # 5 - Final/Game Over; 6 - Final; 7 - Final
        txt_game_status = f"{nhl.ico['finished']} <b>Finished:</b> {'' if linescore['currentPeriod'] == 3 else linescore['currentPeriodOrdinal']}"
        txt_team_away_score = schedule.get_game_team_score_text(team_away_score)
        txt_team_home_score = schedule.get_game_team_score_text(team_home_score)
        txt_game_summary = game_summary_text(data)
        txt_game_details = f"{game_plays_details_text(live['plays'], details)}"

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
def game_plays_details_text(plays, type_plays: str):
    all_plays = plays['allPlays']
    list_plays = plays[type_plays]

    txt = ''

    match type_plays:
        case 'scoringPlays': # Изменение счёта
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
            txt += f"{nhl.ico['penalty']} <b>Penalties:</b>\n"

            for idx_play in list_plays:
                penalty = all_plays[idx_play]

                penalty_time = f"{penalty['about']['ordinalNum']}/{penalty['about']['periodTime']}"  # Время нарушения (период/м:с)
                penalty_team = f"{penalty['team']['triCode']}"  # Команда нарушителя
                penalty_minutes = penalty['result']['penaltyMinutes']  # Срок отбывания нарушения
                penalty_desc = penalty['result']['description']  # Описание нарушения

                txt += f"\n<b>{penalty_time}</b> ({penalty_team}) ({penalty_minutes} min.) {nhl.ico['penalty']} {penalty_desc}\n"

    return txt


# Формирование теста для вывода итоговой информации
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
    txt += f"{team_away_name} |  vs   | {team_home_name}\n" \
           f"{str(team_away_stats['goals']).rjust(widht_1st_field)} | Goals | {team_home_stats['goals']}\n" \
           f"{str(team_away_stats['shots']).rjust(widht_1st_field)} | Shots | {team_home_stats['shots']}\n" \
           f"{str(team_away_stats['hits']).rjust(widht_1st_field)} | Hits  | {team_home_stats['hits']}\n" \
           f"{str(team_away_stats['pim']).rjust(widht_1st_field)} | PIM   | {team_home_stats['pim']}\n" \
           f"{team_away_stats_pp.rjust(widht_1st_field)} | PP    | {team_home_stats_pp}"
    txt += '</code>'

    return txt

