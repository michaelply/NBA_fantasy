import numpy as np
import pandas as pd
import datetime
pd.set_option('display.max_columns', 999)

# Read csv data
all_game_data = pd.read_csv('2019_20_all_game_data.csv')
boxscore_tracker = pd.read_csv('2019_20_boxscore_player_track_df.csv')
boxscore_scoring = pd.read_csv('2019_20_boxscore_scoring_df.csv')

# What the data looks like
all_game_data.head()
all_game_data.dtypes
boxscore_tracker.head()
boxscore_tracker.dtypes
boxscore_scoring.head()
boxscore_scoring.dtypes

# Create datetime object from date string
all_game_data.GAME_DATE = pd.to_datetime(all_game_data.GAME_DATE, format='%b %d, %Y')

# Merge boxscore objects
boxscore = boxscore_tracker.merge(boxscore_scoring, how='inner', on=['GAME_ID', 'TEAM_ID', 'PLAYER_ID'])

# Add GAME DATE column to boxcore
boxscore = boxscore.merge(all_game_data[['Game_ID', 'GAME_DATE']].drop_duplicates(subset=['Game_ID']), how='left', left_on='GAME_ID', right_on='Game_ID')
boxscore.drop(columns=['Game_ID'], inplace=True)

boxscore['GAME_WEEK'] = boxscore['GAME_DATE'].apply(lambda x: x.week)
boxscore['GAME_YEAR'] = boxscore['GAME_DATE'].apply(lambda x: x.year)

groupby_df = boxscore.groupby(['GAME_WEEK', 'PLAYER_ID']).agg({'PLAYER_NAME_x': 'first', 'RBC': 'mean', 'AST': 'mean'}).reset_index()

groupby_df[groupby_df['GAME_WEEK'] == 1].sort_values(by='AST', ascending=False).head(25)