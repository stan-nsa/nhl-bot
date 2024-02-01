# https://records.nhl.com/site/api/franchise
# All players: https://records.nhl.com/site/api/player/

# Goalie:
# https://records.nhl.com/site/api/goalie-season-stats?cayenneExp=seasonId=20222023
# https://records.nhl.com/site/api/goalie-season-stats?cayenneExp=seasonId=20222023&sort=wins&direction=DESC
# https://records.nhl.com/site/api/goalie-season-stats?cayenneExp=seasonId=20222023&sort=goalsAgainstAverage&direction=ASC
# https://records.nhl.com/site/api/goalie-season-stats?cayenneExp=seasonId=20222023&sort=gamesPlayed&direction=DESC

# https://api.nhle.com/stats/rest/en/goalie/summary?isAggregate=false&isGame=false&sort=[{"property":"wins","direction":"DESC"},{"property":"savePct","direction":"DESC"}]&start=0&limit=50&factCayenneExp=gamesPlayed>=1&cayenneExp=gameTypeId=2 and seasonId<=20222023 and seasonId>=20222023
# desired stats: S/C(Shoots/Catches), GP, GS, W, L, OT (Overtime Losses), SA (Shots Against), Svs (Saves), GA (Goals Against), Sv% (Save %) GAA (Goals-Against-Avg), TOI, PIM
# https://api.nhle.com/stats/rest/en/goalie/summary?isAggregate=false&isGame=false&sort=[{"property":"wins","direction":"DESC"},{"property":"savePct","direction":"DESC"}]&start=0&limit=50&factCayenneExp=gamesPlayed>=1&cayenneExp=franchiseId=16 and gameTypeId=2 and seasonId<=20222023 and seasonId>=20222023

# Skater:
# https://records.nhl.com/site/api/skater-playoff-scoring?cayenneExp=seasonId=20212022&sort=points&direction=DESC
# https://records.nhl.com/site/api/skater-playoff-scoring?cayenneExp=seasonId=20212022&sort=goals&direction=DESC
# https://records.nhl.com/site/api/skater-playoff-scoring?cayenneExp=seasonId=20212022&sort=gamesPlayed&direction=DESC

# https://api.nhle.com/stats/rest/en/skater/summary?isAggregate=false&isGame=false&sort=[{"property":"points","direction":"DESC"},{"property":"goals","direction":"DESC"},{"property":"assists","direction":"DESC"}]&start=0&limit=50&factCayenneExp=gamesPlayed>=1&cayenneExp=franchiseId%3D32 and gameTypeId=2 and seasonId<=20192020 and seasonId>=20192020
# https://api.nhle.com/stats/rest/en/skater/summary?isAggregate=false&isGame=false&sort=[{"property":"points","direction":"DESC"},{"property":"goals","direction":"DESC"},{"property":"assists","direction":"DESC"}]&start=0&limit=50&factCayenneExp=gamesPlayed>=1&cayenneExp=franchiseId=16 and gameTypeId=2 and seasonId<=20222023 and seasonId>=20222023
# https://api.nhle.com/stats/rest/en/skater/summary?isAggregate=false&isGame=false&sort=[{"property":"points","direction":"DESC"},{"property":"goals","direction":"DESC"},{"property":"assists","direction":"DESC"}]&start=0&limit=50&factCayenneExp=gamesPlayed>=1&cayenneExp=gameTypeId=2 and seasonId<=20222023 and seasonId>=20222023
# Def https://api.nhle.com/stats/rest/en/skater/summary?isAggregate=false&isGame=false&sort=[{"property":"points","direction":"DESC"}]&start=0&limit=50&factCayenneExp=gamesPlayed>=1&cayenneExp=gameTypeId=2 and seasonId<=20222023 and seasonId>=20222023 and positionCode="D"
# Rookie https://api.nhle.com/stats/rest/en/skater/summary?isAggregate=false&isGame=false&sort=[{"property":"points","direction":"DESC"}]&start=0&limit=50&factCayenneExp=gamesPlayed>=1&cayenneExp=gameTypeId=2 and seasonId<=20222023 and seasonId>=20222023 and isRookie=1


# Teams:
# https://api.nhle.com/stats/rest/en/team/summary?isAggregate=false&isGame=false&sort=[{"property":"points","direction":"DESC"}]&start=0&limit=10&cayenneExp=gameTypeId=2 and seasonId=20222023
# https://api.nhle.com/stats/rest/en/team/summary?isAggregate=false&isGame=false&sort=[{"property":"powerPlayPct","direction":"DESC"}]&start=0&limit=10&cayenneExp=gameTypeId=2 and seasonId=20222023
# https://api.nhle.com/stats/rest/en/team/summary?isAggregate=false&isGame=false&sort=[{"property":"penaltyKillPct","direction":"DESC"}]&start=0&limit=10&cayenneExp=gameTypeId=2 and seasonId=20222023
# https://api.nhle.com/stats/rest/en/team/summary?cayenneExp=gameTypeId=2 and seasonId=20232024 and teamId=4

# https://api.nhle.com/stats/rest/en/franchise?sort=fullName&include=lastSeason.id&include=firstSeason.id
# https://api.nhle.com/stats/rest/en/shiftcharts?cayenneExp=gameId=

# Player image URLs
#        https://nhl.bamcontent.com/images/headshots/current/168x168/###.jpg";  // Image URL for for player 8471675 (Sidney Crosby): https://nhl.bamcontent.com/images/headshots/current/168x168/8471675@2x.jpg
#        https://nhl.bamcontent.com/images/headshots/current/168x168/###@2x.jpg";  // Image URL for 2x size for player 8471675 (Sidney Crosby): https://nhl.bamcontent.com/images/headshots/current/168x168/8471675@2x.jpg
#        https://nhl.bamcontent.com/images/headshots/current/168x168/###@3x.jpg"; // Image URL for 3x size for player 8471675 (Sidney Crosby): https://nhl.bamcontent.com/images/headshots/current/168x168/8471675@2x.jpg


from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from nhl import nhl, stats
from nhl import keyboards


#-- Leaders ---------------------------------------------------------------------------------------
async def command_stats(message: types.Message):
    await message.answer(
        f"{nhl.ico['stats']}<b>Players Stats - Leaders:</b>",
        parse_mode="HTML",
        reply_markup=keyboards.keyboard_stats_gameType())


async def command_stats_leaders_kb(callback: types.CallbackQuery):
    gameType = callback.data.split('_')[2]

    await callback.message.edit_text(f"{nhl.ico['stats']}<b>Players Stats - Leaders({nhl.gameType[gameType]['name']}):</b>", parse_mode="HTML")
    await command_stats_skaters(callback.message, gameType=gameType)
    await command_stats_goalies(callback.message, gameType=gameType)
    await command_stats_defensemen(callback.message, gameType=gameType)
    await command_stats_rookies(callback.message, gameType=gameType)


#-- Skaters ---------------------------------------------------------------------------------------
async def command_stats_skaters(message: types.Message, gameType='regular'):
    await message.answer(
        f"{nhl.ico['skater']}{nhl.ico['stats']}<b>Skaters Stats({nhl.gameType[gameType]['name']}):</b>\n{stats.get_stats_skaters_byProperty_text(property='points', full=False, gameType=gameType)}",
        parse_mode="HTML",
        reply_markup=keyboards.keyboard_stats_skaters(gameType))


async def command_stats_skaters_kb(callback: types.CallbackQuery, gameType='regular'):
    cb_data = callback.data.split('_')
    stata = cb_data[2]
    gameType = cb_data[3]

    try:
        #await callback.message.answer(
        await callback.message.edit_text(
            f"{nhl.ico['skater']}{nhl.ico['stats']}<b>Skaters Stats({nhl.gameType[gameType]['name']}):</b>\n{stats.get_stats_skaters_byProperty_text(property=stata, full=False, gameType=gameType)}",
            parse_mode="HTML",
            reply_markup=keyboards.keyboard_stats_skaters(gameType))

        await callback.answer()

    except:
        await callback.answer()


#-- Goalies ---------------------------------------------------------------------------------------
async def command_stats_goalies(message: types.Message, gameType='regular'):
    await message.answer(
        f"{nhl.ico['goalie']}{nhl.ico['stats']}<b>Goalies Stats({nhl.gameType[gameType]['name']}):</b>\n{stats.get_stats_goalies_byProperty_text(property='goalsAgainstAverage', direction='ASC', full=False, gameType=gameType)}",
        parse_mode="HTML",
        reply_markup=keyboards.keyboard_stats_goalies(gameType))


async def command_stats_goalies_kb(callback: types.CallbackQuery, gameType='regular'):
    cb_data = callback.data.split('_')
    stata = cb_data[2]
    direction = cb_data[3]
    gameType = cb_data[4]

    try:
        #await callback.message.answer(
        await callback.message.edit_text(
            f"{nhl.ico['goalie']}{nhl.ico['stats']}<b>Goalies Stats({nhl.gameType[gameType]['name']}):</b>\n{stats.get_stats_goalies_byProperty_text(property=stata, direction=direction, full=False, gameType=gameType)}",
            parse_mode="HTML",
            reply_markup=keyboards.keyboard_stats_goalies(gameType))

        await callback.answer()

    except:
        await callback.answer()


#-- Defensemen ------------------------------------------------------------------------------------
async def command_stats_defensemen(message: types.Message, gameType='regular'):
    await message.answer(
        f"{nhl.ico['skater']}{nhl.ico['stats']}<b>Defensemen Stats({nhl.gameType[gameType]['name']}):</b>\n{stats.get_stats_defensemen_byProperty_text(property='points', full=False, gameType=gameType)}",
        parse_mode="HTML",
        reply_markup=keyboards.keyboard_stats_defensemen(gameType))


async def command_stats_defensemen_kb(callback : types.CallbackQuery, gameType='regular'):
    stata = callback.data.split('_')[2]
    gameType = callback.data.split('_')[3]

    try:
        #await callback.message.answer(
        await callback.message.edit_text(
            f"{nhl.ico['skater']}{nhl.ico['stats']}<b>Defensemen Stats({nhl.gameType[gameType]['name']}):</b>\n{stats.get_stats_defensemen_byProperty_text(property=stata, full=False, gameType=gameType)}",
            parse_mode="HTML",
            reply_markup=keyboards.keyboard_stats_defensemen(gameType))

        await callback.answer()

    except:
        await callback.answer()


#-- Rookies ---------------------------------------------------------------------------------------
async def command_stats_rookies(message: types.Message, gameType='regular'):
    await message.answer(
        f"{nhl.ico['skater']}{nhl.ico['stats']}<b>Rookies Stats({nhl.gameType[gameType]['name']}):</b>\n{stats.get_stats_rookies_byProperty_text(property='points', full=False, gameType=gameType)}",
        parse_mode="HTML",
        reply_markup=keyboards.keyboard_stats_rookies(gameType))


async def command_stats_rookies_kb(callback: types.CallbackQuery, gameType='regular'):
    cb_data = callback.data.split('_')
    stata = cb_data[2]
    gameType = cb_data[3]

    try:
        #await callback.message.answer(
        await callback.message.edit_text(
            f"{nhl.ico['skater']}{nhl.ico['stats']}<b>Rookies Stats({nhl.gameType[gameType]['name']}):</b>\n{stats.get_stats_rookies_byProperty_text(property=stata, full=False, gameType=gameType)}",
            parse_mode="HTML",
            reply_markup=keyboards.keyboard_stats_rookies(gameType))

        await callback.answer()

    except:
        await callback.answer()


#-- Teams -----------------------------------------------------------------------------------------
async def command_stats_teams(message: types.Message, gameType='regular'):
    await message.answer(
        f"{nhl.ico['stats']}<b>Teams Stats:</b>",
        parse_mode="HTML",
        reply_markup=keyboards.keyboard_stats_teams_gameType())


async def command_stats_teams_kb(callback : types.CallbackQuery, gameType='regular'):
    cb_data = callback.data.split('_')

    if cb_data[2] in nhl.gameType.keys():
        stata = 'wins'
        direction = 'DESC'
        gameType = cb_data[2]
    else:
        stata = cb_data[2]
        direction = cb_data[3]
        gameType = cb_data[4]

    try:
        #await callback.message.answer(
        await callback.message.edit_text(
            f"{nhl.ico['stats']}<b>Teams Stats({nhl.gameType[gameType]['name']}):</b>\n{stats.get_stats_teams_byProperty_text(property=stata, direction=direction, full=False, gameType=gameType)}",
            parse_mode="HTML",
            reply_markup=keyboards.keyboard_stats_teams(gameType))

        await callback.answer()

    except:
        await callback.answer()


#-- Register Handlers -----------------------------------------------------------------------------
def register_handlers_stats(dp : Dispatcher):
    dp.register_message_handler(command_stats, commands=['stats'])
    dp.register_message_handler(command_stats_skaters, commands=['stats_skaters'])
    dp.register_message_handler(command_stats_goalies, commands=['stats_goalies'])
    dp.register_message_handler(command_stats_defensemen, commands=['stats_defensemen'])
    dp.register_message_handler(command_stats_rookies, commands=['stats_rookies'])
    dp.register_message_handler(command_stats_teams, commands=['stats_teams'])
    dp.register_callback_query_handler(command_stats_leaders_kb, Text(startswith='stats_leaders_'))
    dp.register_callback_query_handler(command_stats_skaters_kb, Text(startswith='stats_skaters_'))
    dp.register_callback_query_handler(command_stats_goalies_kb, Text(startswith='stats_goalies_'))
    dp.register_callback_query_handler(command_stats_defensemen_kb, Text(startswith='stats_defensemen_'))
    dp.register_callback_query_handler(command_stats_rookies_kb, Text(startswith='stats_rookies_'))
    dp.register_callback_query_handler(command_stats_teams_kb, Text(startswith='stats_teams_'))

