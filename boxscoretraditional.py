from nba_api.stats.endpoints import boxscoretraditionalv2
import pandas as pd
import time

all_game_data = pd.read_csv('2019_20_all_game_data.csv')

all_game_id = pd.DataFrame(all_game_data['Game_ID'].unique()).reset_index()

appended_data = []

for i in range(0, len(all_game_id)):
    print('Getting boxscore traditional for ' + str(i) + ' ...')
    appended_data.append(pd.DataFrame(boxscoretraditionalv2.BoxScoreTraditionalV2(game_id = '00' + str(all_game_id[0][i])).get_data_frames()[0]))
    time.sleep(3)

box_score_data = pd.concat(appended_data)

# write to csv

box_score_data.to_csv('2019_20_boxscore_traditional_df.csv', index=False)