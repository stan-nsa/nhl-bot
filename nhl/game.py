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

    txt = f"{nhl.ico['schedule']} <b>{schedule.get_game_time_tz_text(game['datetime']['dateTime'], withDate=True, withTZ=True)}:</b>\n"

    away_team = game['teams']['away']['name']  # ['abbreviation']
    home_team = game['teams']['home']['name']  # ['abbreviation']

    # Scheduled
    if int(game['status']['statusCode']) < 3:  # 1 - Scheduled; 2 - Pre-Game
        txt += f"{nhl.ico['time']} <b>Scheduled:</b>\n"
        txt += f"{away_team}{nhl.ico['vs']}{home_team}" \
               f"{nhl.ico['time']}{schedule.get_game_time_tz_text(game['datetime']['dateTime'], withTZ=True)}\n"
    # Live
    elif int(game['status']['statusCode']) < 5:  # 3 - Live/In Progress; 4 - Live/In Progress - Critical
        txt += f"{nhl.ico['live']} <b>Live: {linescore['currentPeriodOrdinal']} / {linescore['currentPeriodTimeRemaining']}</b>\n"
        txt += f"{get_game_teams_score_text(linescore)}\n"
        txt += f"{game_plays_details_text(live['plays'], details)}"

    # Final
    elif int(game['status']['statusCode']) < 8:  # 5 - Final/Game Over; 6 - Final; 7 - Final
        txt += f"\n{nhl.ico['finished']} <b>Finished:</b> {'' if linescore['currentPeriod'] == 3 else linescore['currentPeriodOrdinal']}\n"
        txt += f"{get_game_teams_score_text(linescore)}\n"
        txt += f"{game_plays_details_text(live['plays'], details)}"

    # TBD/Postponed
    elif int(game['status']['statusCode']) < 10:  # 8 - Scheduled (Time TBD); 9 - Postponed
        txt += f"{away_team}{nhl.ico['vs']}{home_team} " \
               f"{nhl.ico['tbd']} {game['status']['detailedState']}\n"
    # Other
    else:
        txt += f"{away_team}{nhl.ico['vs']}{home_team}\n"

    return txt


def get_game_teams_score_text(linescore):

    away_team = linescore['teams']['away']['team']['name'] #['abbreviation']
    away_team_score = linescore['teams']['away']['goals']

    home_team = linescore['teams']['home']['team']['name']  #['abbreviation']
    home_team_score = linescore['teams']['home']['goals']

    #game_teams_score = f"{away_team} {schedule.get_game_team_score_text(away_team_score, hideScore=False)}{emojize(':ice_hockey:')}{schedule.get_game_team_score_text(home_team_score, hideScore=False)} {home_team}"
    game_teams_score = f"{schedule.get_game_team_score_text(away_team_score, hideScore=False)} {away_team}\n{schedule.get_game_team_score_text(home_team_score, hideScore=False)} {home_team}"

    return game_teams_score


# Формирование теста для детального вывода информации по определенному виду событий (scoringPlays, penaltyPlays)
def game_plays_details_text(plays, type_plays: str):
    all_plays = plays['allPlays']
    list_plays = plays[type_plays]

    txt = ''
    for idx_play in list_plays:

        match type_plays:
            case 'scoringPlays':
                score = all_plays[idx_play]

                if (score['about']['periodType'] == 'SHOOTOUT'):
                    continue

                score_teams = f"{score['about']['goals']['away']}:{score['about']['goals']['home']}"    # Счёт
                score_team = f"{score['team']['triCode']}"  # Забившая команда
                score_time = f"{score['about']['ordinalNum']}/{score['about']['periodTime']}"   # Время изменения счёта (период/м:с)
                score_strength = f"({score['result']['strength']['code']}) " if (score['result']['strength']['code'] != 'EVEN') else '' # Вывод PPG или SHG
                score_players = score['result']['description'] #.split(', assists: ')

                txt += f"\n<b>{score_teams}</b> ({score_team}) ({score_time}) {nhl.ico['goal']} {score_strength}{score_players}\n"

            case 'penaltyPlays':
                penalty = all_plays[idx_play]

                penalty_time = f"{penalty['about']['ordinalNum']}/{penalty['about']['periodTime']}"  # Время нарушения (период/м:с)
                penalty_team = f"{penalty['team']['triCode']}"  # Команда нарушителя
                penalty_desc = penalty['result']['description']  # Описание нарушения
                penalty_minutes = penalty['result']['penaltyMinutes']  # Срок отбывания нарушения

                txt += f"\n<b>{penalty_time}</b> ({penalty_team}) ({penalty_minutes} min.) {nhl.ico['penalty']} {penalty_desc}\n"

            case _:
                continue

    return txt
