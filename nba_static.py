import pandas as pd
from nba_api.stats.static import teams, players

nba_teams = teams.get_teams()

nba_teams_df = pd.DataFrame({'ID': [team['id'] for team in nba_teams],
                             'Full_name': [team['full_name'] for team in nba_teams],
                             'Abbreviation': [team['abbreviation'] for team in nba_teams],
                             'Nickname': [team['nickname'] for team in nba_teams],
                             'City': [team['city'] for team in nba_teams],
                             'State': [team['state'] for team in nba_teams],
                             'Year_founded': [team['id'] for team in nba_teams]
                             })

# write to csv
nba_teams_df.to_csv('nba_teams_df.csv', index=False)

nba_players = players.get_players()

nba_players_df = pd.DataFrame({'ID': [player['id'] for player in nba_players],
                               'Full_name': [player['full_name'] for player in nba_players],
                               'First_name': [player['first_name'] for player in nba_players],
                               'Last_name': [player['last_name'] for player in nba_players],
                               'Active_flag': [player['is_active'] for player in nba_players]})

# write to csv
nba_players_df.to_csv('nba_players_df.csv', index=False)



