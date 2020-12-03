import numpy as np
import pandas as pd
import datetime
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)

# Read traditional box score csv file
boxscore = pd.read_csv('2019_20_boxscore_traditional_df.csv')
all_game_data = pd.read_csv('2019_20_all_game_data.csv')

"""
2019_20_boxscore_traditional_df is a csv file which contains statistics collected by each player in every single game
they played in the 2019-2020 NBA season.

Useful columns:
1. GAME_ID - Unique game identifier (2 teams played against each other would have the same GAME_ID)
2. PLAYER_NAME - Unique NBA player identifier (assume no player has same name)
3. COMMENT - Explanation on why a player has no data (only if he was on the roster)
4. FGA - Field Goal Attempted
5. FGM - Field Goal Made
6. FG3M - 3 Pointers Made 
7. FTA - Free Throws Attempted
8. FTM - Free Throws Made
9. REB - Rebounds
10. AST - Assists
11. STL - Steals
12. BLK - Blocks
13. PTS - Points

Method:
There are 8 categories in Fantasy Basketball League as follow:
1.FG% 2.FT% 3.PTS 4.AST 5.REB 6.STL 7.BLK 8.3PM

We aggregate a weekly average of FGA, FGM, FG3M, FTA, FTM, PTS, REB, AST, STL, BLK for each NBA player, then calculate
their percentile among all players in PTS, AST, REB, STL, BLK and 3PM.
For FG% and FT%, we use a different approach because bias might occur for percentages. For example, if player 1
attempted and made 1 shot, and player 2 made 9 out of 10, player 1 would rank over player 2 even though player 2
should be consider a "better" player. Therefore, we develop a different matrix to solve this issue. This new metric
takes the average of shooting percentage percentile and number of attempts percentile.
FG% Metric = [FG%(percentile) + FGA(percentile)]/2
FT% Metric = [FT%(percentile) + FTA(percentile)]/2


Steps:
1. Group game log data by week and aggregate game statistics average
2. Calculate weekly percentiles
3. Group by player and aggregate average percentiles
"""
boxscore.head()
boxscore.columns

all_game_data.columns

# Merge boxscore with all_game_data to get GAME_DATE column
all_game_data[['Game_ID','GAME_DATE']].head()
boxscore = boxscore.merge(all_game_data[['Game_ID', 'GAME_DATE']].drop_duplicates(subset=['Game_ID']), how='left', left_on='GAME_ID', right_on='Game_ID')

boxscore.drop(columns=['Game_ID'], inplace=True)

len(boxscore)
boxscore.head()

# Create GAME_WEEK and GAME_YEAR columns from GAME_DATE
boxscore.GAME_DATE = pd.to_datetime(boxscore.GAME_DATE, format='%b %d, %Y')
boxscore['GAME_WEEK'] = boxscore['GAME_DATE'].apply(lambda x: x.week)
boxscore['GAME_YEAR'] = boxscore['GAME_DATE'].apply(lambda x: x.year)
boxscore.head()
boxscore.columns

# How many games were played in the 2019/2020 NBA season?
total_games = len(boxscore.GAME_ID.unique())
total_games

# How many games were played per team?
number_of_teams = 30
teams_per_game = 2
total_games/number_of_teams*teams_per_game # ~55 games were played in the season per NBA team

# Remove players who played less then 45 games (55 total)
# 1. Player's game log exists but he didn't play at all
boxscore.drop(boxscore[pd.isnull(boxscore.MIN)].index,inplace=True)

# 2. Player's game log not in record
player_list = boxscore.PLAYER_NAME.unique()
for player in player_list:
    if len(boxscore[boxscore.PLAYER_NAME == player]) < 45:
        boxscore.drop(boxscore[boxscore.PLAYER_NAME == player].index, inplace=True)

len(boxscore)

# Aggregate to weekly boxscore data
weekly_boxscore = boxscore.groupby(['GAME_WEEK', 'PLAYER_ID', 'PLAYER_NAME']).agg({'PTS': 'mean', 'REB': 'mean', 'AST': 'mean', 'STL': 'mean', 'BLK': 'mean', 'FG3M': 'mean', 'FGA': 'sum', 'FGM': 'sum', 'FTA': 'sum', 'FTM': 'sum'}).reset_index()

# Calculate weekly FG% and FT%
weekly_boxscore['FG_PCT'] = weekly_boxscore['FGM']/weekly_boxscore['FGA']
weekly_boxscore['FT_PCT'] = weekly_boxscore['FTM']/weekly_boxscore['FTA']

weekly_boxscore.head()

# Create a list which each element represents a weekly boxscore dataframe
def CreateWeeklyBoxscoreDfList(df):
    weekly_boxscore_df = []
    game_week = list(weekly_boxscore.GAME_WEEK.unique())
    for week in game_week:
        weekly_boxscore_df.append(df[df['GAME_WEEK'] == week])

    return weekly_boxscore_df

weekly_boxscore_df_list = CreateWeeklyBoxscoreDfList(weekly_boxscore)
len(weekly_boxscore_df_list)
weekly_boxscore_df_list

def CreatePercentileColumn(df, colname):
    percentile_column = colname + '_PERCENTILE'
    df[percentile_column] = df[colname].rank(pct=True)
    return df

for weekly_boxscore in weekly_boxscore_df_list:
    CreatePercentileColumn(weekly_boxscore, 'PTS')
    CreatePercentileColumn(weekly_boxscore, 'REB')
    CreatePercentileColumn(weekly_boxscore, 'AST')
    CreatePercentileColumn(weekly_boxscore, 'STL')
    CreatePercentileColumn(weekly_boxscore, 'BLK')
    CreatePercentileColumn(weekly_boxscore, 'FG3M')
    CreatePercentileColumn(weekly_boxscore, 'FGA')
    CreatePercentileColumn(weekly_boxscore, 'FG_PCT')
    CreatePercentileColumn(weekly_boxscore, 'FTA')
    CreatePercentileColumn(weekly_boxscore, 'FT_PCT')

# Create new FG and FT metrics by averaging attempts and shooting percentages percentiles
for weekly_boxscore in weekly_boxscore_df_list:
    weekly_boxscore['FG_PCT_METRIC'] = (weekly_boxscore['FGA_PERCENTILE'] + weekly_boxscore['FG_PCT_PERCENTILE'])/2
    weekly_boxscore['FT_PCT_METRIC'] = (weekly_boxscore['FTA_PERCENTILE'] + weekly_boxscore['FT_PCT_PERCENTILE'])/2

# Aggregate weekly boxscore to seansonal average
weekly_boxscore = pd.DataFrame()
for df in weekly_boxscore_df_list:
    weekly_boxscore = weekly_boxscore.append(df)
seasonal_boxscore = weekly_boxscore.groupby(['PLAYER_ID']).agg({'PLAYER_NAME': 'first', 'PTS_PERCENTILE': 'mean', 'REB_PERCENTILE': 'mean', 'AST_PERCENTILE': 'mean', 'STL_PERCENTILE': 'mean', 'BLK_PERCENTILE': 'mean', 'FG3M_PERCENTILE': 'mean', 'FG_PCT_METRIC': 'mean', 'FT_PCT_METRIC': 'mean'})

# Calculate player FANTASY_SCORE by summing up all stats categories' percentiles
seasonal_boxscore['FANTASY_SCORE'] = seasonal_boxscore['PTS_PERCENTILE']+seasonal_boxscore['AST_PERCENTILE']+seasonal_boxscore['REB_PERCENTILE']+seasonal_boxscore['STL_PERCENTILE']+seasonal_boxscore['BLK_PERCENTILE']+seasonal_boxscore['FG3M_PERCENTILE']+seasonal_boxscore['FG_PCT_METRIC']+seasonal_boxscore['FT_PCT_METRIC']

# Top 50 Performers
top_50_fantasy_pick = seasonal_boxscore.sort_values(by='FANTASY_SCORE', ascending=False).head(50)[['PLAYER_NAME','FANTASY_SCORE']]
top_50_fantasy_pick

# Top 5 Players Overview
seasonal_boxscore.sort_values(by='FANTASY_SCORE', ascending=False).head()