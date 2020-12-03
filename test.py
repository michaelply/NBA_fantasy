import pandas as pd
from nba_api.stats.static import teams, players

nba_teams = teams.get_teams()
nba_players = players.get_active_players()

# Select the dictionary for the Pacers, which contains their team ID
pacers = [team for team in nba_teams if team['abbreviation'] == 'INC'][0]
pacers_id = pacers['id']
print(f'pacers_id: {pacers_id}')

okc = [team for team in nba_teams if team['abbreviation'] == 'OKC'][0]
okc_id = okc['id']


mia = [team for team in nba_teams if team['abbreviation'] == 'MIA'][0]
mia_id = mia['id']


# Query for the last regular season game where the Pacers were playing
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.library.parameters import Season
from nba_api.stats.library.parameters import SeasonType

gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=pacers_id,
                            season_nullable=Season.default,
                            season_type_nullable=SeasonType.regular)

games_dict = gamefinder.get_normalized_dict()
games = games_dict['LeagueGameFinderResults']
game = games[0]
game_id = game['GAME_ID']
game_matchup = game['MATCHUP']

print(f'Searching through {len(games)} game(s) for the game_id of {game_id} where {game_matchup}')


# Query for the play by play of that most recent regular season game
from nba_api.stats.endpoints import playbyplay
df = playbyplay.PlayByPlay(game_id).get_data_frames()[0]
df.head() #just looking at the head of the data

from nba_api.stats.endpoints import shotchartdetail, shotchartlineupdetail, playerdashptshots, playercareerstats

shot_df = shotchartdetail.ShotChartDetail(team_id = mia_id, player_id= '1628389').get_data_frames()[0]

player_career = playercareerstats.PlayerCareerStats(player_id='1628389').get_data_frames()[0]


shotchartlineupdetail.ShotChartLineupDetail()
