# https://api-web.nhle.com/v1/gamecenter/2023020206/landing
# https://api-web.nhle.com/v1/gamecenter/2023020204/boxscore

from nhl import nhl
from nhl import schedule
from nhl import stats


#== Получение от сервера данных о матче ===========================================================

# Получение от сервера данных о матче
def get_game_data(game_id):

    data = {'boxscore': {}, 'landing': {}}

    game_boxscore_str = f"gamecenter/{game_id}/boxscore"
    game_landing_str = f"gamecenter/{game_id}/landing"

    data['boxscore'] = nhl.get_request_nhl_api(game_boxscore_str)
    data['landing'] = nhl.get_request_nhl_api(game_landing_str)

    return data


# Формирование теста для вывода информации о матче
def get_game_text(game_id, details='scoring'):
    data = get_game_data(game_id)

    boxscore = data.get('boxscore')
    landing = data.get('landing')

    txt_game_summary = ''
    txt_game_details = ''
    txt_team_away_score = ''
    txt_team_home_score = ''

    team_away = f"{landing.get('awayTeam').get('placeName').get('default')} {boxscore.get('awayTeam').get('name').get('default')}"
    team_home = f"{landing.get('homeTeam').get('placeName').get('default')} {boxscore.get('homeTeam').get('name').get('default')}"

    # -- Статистика команд --
    team_away_w_l_o = team_home_w_l_o = ''
    query_str = f"team/summary?cayenneExp=gameTypeId={boxscore.get('gameType')} and seasonId={boxscore.get('season')} and teamId in ({boxscore.get('awayTeam').get('id')},{boxscore.get('homeTeam').get('id')})"
    data_stats = stats.get_request_nhl_stats_api(query_str).get('data')
    if len(data_stats) > 1:
        team_away_stats = data_stats[0] if (data_stats[0].get('teamId') == boxscore.get('awayTeam').get('id')) else data_stats[1]
        team_home_stats = data_stats[1] if (data_stats[1].get('teamId') == boxscore.get('homeTeam').get('id')) else data_stats[0]

        #-- Статистика команд на момент матча: (wins-losses-ot) --
        team_away_w_l_o = f"({team_away_stats.get('wins')}-{team_away_stats.get('losses')}" + \
                          (f"-{team_away_stats.get('otLosses')})" if (boxscore.get('gameType') == nhl.gameType.get('regular').get('id')) else f")")
        team_home_w_l_o = f"({team_home_stats.get('wins')}-{team_home_stats.get('losses')}" + \
                          (f"-{team_home_stats.get('otLosses')})" if (boxscore.get('gameType') == nhl.gameType.get('regular').get('id')) else f")")

    # -- Информация о текущей серии ПО (Game #, Team lead) --
    series_summary = ""
    # if boxscore.get('gameType') == nhl.gameType.get('playoff').get('id'):
    #     query_str = f"club-schedule/{boxscore.get('awayTeam').get('abbrev')}/week/{boxscore.get('gameDate')}"
    #     data_series = nhl.get_request_nhl_api(query_str)
    #     series_status = data_series.get('games')[0].get('seriesStatus')
    #
    #     if series_status.get('awayTeamWins') == series_status.get('homeTeamWins'):
    #         series_score = "Tied"
    #     elif series_status.get('awayTeamWins') > series_status.get('homeTeamWins'):
    #         series_score = f"{boxscore.get('awayTeam').get('abbrev')}"
    #     else:
    #         series_score = f"{boxscore.get('homeTeam').get('abbrev')}"
    #
    #     series_score += f" {series_status.get('awayTeamWins')}-{series_status.get('homeTeamWins')}"
    #
    #     series_summary = f"({series_status.get('roundAbbrev')} G{series_status.get('gameNumberOfSeries')} | {series_score})"
    # --------------------------------------------------------

    # Scheduled
    if boxscore.get('gameState') in nhl.gameState.get('scheduled'):
        txt_game_status = f"{nhl.ico.get('time')} <b>Scheduled:</b> {nhl.ico.get('time')}{schedule.get_game_time_tz_text(boxscore.get('startTimeUTC'), withTZ=True, inlinemenu=True)}"

    # Live
    elif boxscore.get('gameState') in nhl.gameState.get('live'):
        currentPeriod = boxscore.get('periodDescriptor').get('periodType') if boxscore.get('periodDescriptor').get('number') > 3 else nhl.gamePeriods[boxscore.get('periodDescriptor').get('number')]
        txt_game_status = f"{nhl.ico.get('live')} <b>Live: {currentPeriod} / {'END' if (boxscore.get('clock').get('inIntermission')) else boxscore.get('clock').get('timeRemaining')}</b>"
        txt_team_away_score = schedule.get_game_team_score_text(boxscore.get('awayTeam').get('score'))
        txt_team_home_score = schedule.get_game_team_score_text(boxscore.get('homeTeam').get('score'))
        txt_game_summary = game_summary_text(landing)
        txt_game_details = game_details_text(data, details)

    # Final
    elif boxscore.get('gameState') in nhl.gameState.get('final'):
        txt_game_status = f"{nhl.ico.get('finished')} <b>Finished:</b> {'' if boxscore.get('periodDescriptor').get('number') == 3 else boxscore.get('periodDescriptor').get('periodType')}"
        txt_team_away_score = schedule.get_game_team_score_text(boxscore.get('awayTeam').get('score'))
        txt_team_home_score = schedule.get_game_team_score_text(boxscore.get('homeTeam').get('score'))
        txt_game_summary = game_summary_text(landing)
        txt_game_details = game_details_text(data, details)

    # TBD/Postponed
    elif boxscore.get('gameState') in nhl.gameState.get('tbd'):
        txt_game_status = f"{nhl.ico.get('tbd')} <b>{boxscore.get('gameState')}</b>"

    # Other
    else:
        txt_game_status = ""

    #-- Формирование текста вывода информации о матче -----
    txt = f"{nhl.ico.get('schedule')} <b>{schedule.get_game_time_tz_text(boxscore.get('startTimeUTC'), withDate=True, withTZ=True, inlinemenu=True)}:</b>\n"
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
            scoring = data.get('landing').get('summary').get(type_details)

            txt += f"{nhl.ico.get('scores')}{nhl.ico.get('goal')} <b>Scoring:</b>\n"

            for period in scoring:
                period_txt = f"{period.get('periodDescriptor').get('periodType') if (period.get('periodDescriptor').get('number') > 3) else nhl.gamePeriods.get(period.get('periodDescriptor').get('number'))}"
                txt += f"\n<b>{period_txt}{' period' if (period.get('periodDescriptor').get('number') < 4) else ''}:</b>"

                for goal in period.get('goals'):
                    score_teams = f"{goal.get('awayScore')}:{goal.get('homeScore')}"    # Счёт
                    score_team = f"{goal.get('teamAbbrev').get('default')}"  # Забившая команда
                    score_time = f"{goal.get('timeInPeriod')}"  # Время изменения счёта (м:с)
                    score_strength = f"({nhl.goalType.get(goal.get('strength'))}) " if (goal.get('strength') != 'ev') else ''
                    score_player = f"{goal.get('name').get('default')}"
                    score_player_goals = f"({goal.get('goalsToDate')})" if (period.get('periodDescriptor').get('periodType') != 'SO') else ''

                    score_assists = ''
                    for assist in goal.get('assists'):
                        score_assists += ', ' if len(score_assists) else ''
                        score_assists += f"{assist.get('name').get('default')} ({assist.get('assistsToDate')})"

                    txt += f"\n<b>{score_teams}</b> ({score_team}) ({score_time}) {nhl.ico.get('goal')} {score_strength}{score_player} {score_player_goals}\n"
                    txt += f" assists: {score_assists}\n" if len(score_assists) else ''

        case 'penalties': # Нарушения
            penalties = data.get('landing').get('summary').get(type_details)

            txt += f"{nhl.ico.get('penalty')} <b>Penalties:</b>\n"

            for period in penalties:
                period_txt = f"{period.get('periodDescriptor').get('periodType') if (period.get('periodDescriptor').get('number') > 3) else nhl.gamePeriods[period.get('periodDescriptor').get('number')]}"
                txt += f"\n<b>{period_txt}{' period' if (period.get('periodDescriptor').get('number') < 4) else ''}:</b>"

                for penalty in period.get('penalties'):
                    penalty_time = penalty.get('timeInPeriod')  # Время нарушения (период/м:с)
                    penalty_team = penalty.get('teamAbbrev')    # Команда нарушителя
                    penalty_minutes = penalty.get('duration')   # Срок отбывания нарушения
                    penalty_desc = penalty.get('descKey')       # Описание нарушения
                    penalty_player = penalty.get('committedByPlayer', '')   # Оштрафованный игрок

                    txt += f"\n<b>{penalty_time}</b> ({penalty_team}) {nhl.ico.get('penalty')} {penalty_player}: {penalty_desc} ({penalty_minutes} min.)\n"

        case 'teamGameStats':  # Статистика игроков команд
            txt += f"{nhl.ico.get('stats')} <b>Team Stats:</b>\n"
            txt += game_teams_stats_text(data.get('boxscore'))

        case 'gameReports':  # Отчеты
            #reports = data.get('boxscore').get('boxscore').get('gameReports')
            reports = data.get('boxscore').get('summary').get('gameReports')
            txt += f"{nhl.ico.get('report')} <b>Game Reports:</b>\n\n" \
                   f"{nhl.ico.get('point')} <a href='" + reports.get('gameSummary') + "'>Game Summary</a>\n\n" \
                   f"{nhl.ico.get('point')} <a href='" + reports.get('eventSummary') + "'>Event Summary</a>\n\n" \
                   f"{nhl.ico.get('point')} <a href='" + reports.get('rosters') + "'>Club Playing Roster</a>\n\n" \
                   f"{nhl.ico.get('point')} <a href='" + reports.get('shotSummary') + "'>Shot Summary</a>\n\n" \
                   f"{nhl.ico.get('point')} <a href='" + reports.get('toiAway') + f"'>Time On Ice: {data.get('boxscore').get('awayTeam').get('name').get('default')}</a>\n\n" \
                   f"{nhl.ico.get('point')} <a href='" + reports.get('toiHome') + f"'>Time On Ice: {data.get('boxscore').get('homeTeam').get('name').get('default')}</a>"

    return txt


# Формирование теста для вывода итоговой информации о матче
def game_summary_text(data):
    team_away_name = data.get('awayTeam').get('name').get('default')
    team_home_name = data.get('homeTeam').get('name').get('default')

    widht_1st_field = len(team_away_name)
    widht_stats_abbrev_field = 5    # Ширина колонки аббривиатуры статистики

    txt = "<b>Game Summary:</b>\n"
    #txt += '<code>'
    txt += '<pre>'
    txt += f"{team_away_name} | {'vs'.center(widht_stats_abbrev_field)} | {team_home_name}\n" \
           f"{str(data.get('awayTeam').get('score')).rjust(widht_1st_field)} | {'Goals'.center(widht_stats_abbrev_field)} | {data.get('homeTeam').get('score')}\n"

    for stat in data.get('summary').get('teamGameStats'):
        if (stat.get('category') in stats.game_stats):
            txt += f"{str(stat.get('awayValue')).rjust(widht_1st_field)} | {stats.game_stats.get(stat.get('category')).center(widht_stats_abbrev_field)} | {stat.get('homeValue')}\n"

    #txt += '</code>'
    txt += '</pre>'

    return txt


# Формирование теста для вывода статистики игроков
def game_teams_stats_text(data):
    #players_stats = data.get('boxscore').get('playerByGameStats')
    players_stats = data.get('playerByGameStats')

    width_player_name = 17 # Ширина поля имени игрока

    txt = ''

    for team, players_positions in players_stats.items():

        team_name = data[team].get('name').get('default')

        txt += f"\n<b>{team_name}</b>\n"
        # txt += "<code>"
        txt += "<pre>"
        for players_pos, players in players_positions.items():
            if (players_pos == 'goalies'):
                txt += f"_#|{players_pos.center(width_player_name, '_').upper()}|Sv/Sh|_Sv%_|_TOI_\n"  # Шапка таблицы статистики вратарей
            else:
                txt += f"_#|{players_pos.center(width_player_name, '_').upper()}|G|A|+-|S_|PM|_TOI_\n"  # Шапка таблицы статистики полевых

            for player in players:
                player_number = str(player.get('sweaterNumber'))
                player_name = player.get('name').get('default').replace('. ', '.')
                player_name = player_name if (len(player_name) <= width_player_name) else f"{player_name[:width_player_name-3]}..."
                player_toi = player.get('toi')

                txt += f"{player_number.rjust(2)}|" \
                       f"{player_name.ljust(width_player_name)}|"

                if (players_pos == 'goalies'): # Строка статистики вратарей
                    player_ssa = player.get('saveShotsAgainst')
                    player_savePctg = player.get('savePctg') if ('savePctg' in player) else ''

                    txt += f"{player_ssa.center(5)}|" \
                           f"{player_savePctg.center(5)}|"

                else: # Строка статистики полевых
                    player_goals = player.get('goals')
                    player_assists = player.get('assists')
                    player_p_m = f"{'+' if (player.get('plusMinus') > 0) else ''}{player.get('plusMinus')}"
                    player_shots = player.get('shots')
                    player_pim = player.get('pim')

                    txt += f"{player_goals}|" \
                           f"{player_assists}|" \
                           f"{player_p_m.rjust(2)}|" \
                           f"{str(player_shots).rjust(2)}|" \
                           f"{str(player_pim).rjust(2)}|"

                txt += f"{player_toi}\n"

        # txt += "</code>"
        txt += "</pre>"

    return txt
