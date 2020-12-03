from nba_api.stats.endpoints import teamgamelog
import pandas as pd
import time

# load team and players dfs
nba_teams_df = pd.read_csv('nba_teams_df.csv')
nba_players_df = pd.read_csv('nba_players_df.csv')

# Season.default = '2019-20'

appended_data = []

for i in range(0, len(nba_teams_df)):
    print('Getting team log for ' + nba_teams_df['Full_name'][i] + ' ...')
    appended_data.append(pd.DataFrame(teamgamelog.TeamGameLog(team_id=nba_teams_df['ID'][i]).get_data_frames()[0]))
    time.sleep(10)

all_game_data = pd.concat(appended_data)

# write to csv
all_game_data.to_csv('2019_20_all_game_data.csv', index=False)