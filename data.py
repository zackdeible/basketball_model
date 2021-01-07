import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go



st.title('Basketball current season data')

st.write("""
# Dataset

Advanced and basic statistics from every game from the current NBA season.

Test out the different features and follow us on tik tok and twitter to get updates about the app and to leave feedback.

Goal is to help make smarter bets with better data insights. 

	""")




df_team = pd.read_csv('current_nba_team_avgs.csv')

df_quarter = pd.read_csv('per_quarter_stats.csv')

df = pd.read_csv('current_nba_data.csv')


teams = df_team['teams']

home_team = st.selectbox('Choose home team', teams)

away_team = st.selectbox('Choose an away team', teams)
 
if home_team != away_team:
	st.title("Summary statistics")

	st.write(df_team.loc[(df_team['teams']==home_team)][['teams', 'fg_pct', 'fg3_pct', 'efg_pct', 'off_rtg', 'def_rtg', 'score']])
	st.write(df_team.loc[(df_team['teams']==away_team)][['teams', 'fg_pct', 'fg3_pct', 'efg_pct', 'off_rtg', 'def_rtg', 'score']])

	df_home_q = df_quarter.loc[(df_quarter['team']==home_team)]
	df_away_q = df_quarter.loc[(df_quarter['team']==away_team)]

	

	df_home_avgs = df_home_q.groupby('quarter', axis=0).mean().reset_index()
	df_away_avgs = df_away_q.groupby('quarter', axis=0).mean().reset_index()

	df_combined_cols = ['quarter', 'home_team', 'away_team']
	df_combined = pd.concat([df_home_avgs['quarter'], df_home_avgs['pts'], df_away_avgs['pts']], axis=1)
	df_combined.columns = df_combined_cols
	

	fg = px.bar(df_combined, x='quarter', y=['home_team', 'away_team'], title='Over Unders')
	st.plotly_chart(fg)

	fg1 = go.Figure(data=[
		go.Bar(name=home_team, x=df_combined['quarter'], y=df_combined['home_team']),
		go.Bar(name=away_team, x=df_combined['quarter'], y=df_combined['away_team'])])

	fg1.update_layout(barmode='group', title='Spread Difference')
	st.plotly_chart(fg1)

	st.title("Data Table Views")

	st.write("Data Combined",df_combined)

	st.write(home_team.upper()+' Averages',df_home_avgs)
	st.write(away_team.upper()+' Averages', df_away_avgs)

	#feature = st.selectbox('Which feature?', df.loc[(df['team']==home_team)].columns.drop(['mp', 'away_team_x', 'total', 'team', 'money_line', 'away_money_line', 'fg_pct', 'fg3_pct', 'ft_pct', 'away_fg_pct', 'away_fg3_pct', 'ts_pct', 'efg_pct', 'fg3a_per_fga_pct', 'orb_pct', 'drb_pct', 'trb_pct', 'ast_pct', 'stl_pct', 'blk_pct', 'tov_pct', 'usg_pct', 'off_rtg', 'def_rtg', 'score', 'date', 'away_ts_pct', 'away_efg_pct', 'away_fg3a_per_fga_pct', 'away_orb_pct', 'away_drb_pct', 'away_trb_pct', 'away_ast_pct', 'away_stl_pct', 'away_blk_pct', 'away_tov_pct', 'away_usg_pct', 'away_off_rtg', 'away_def_rtg', 'away_score', 'fta_per_fga_pct', 'away_fta_per_fga_pct', 'away_ft_pct']))
	# Filter dataframe
	st.title("Calculate frequency of certain statistics")
	df_full_game = df_quarter.loc[(df_quarter['mp'].astype(int)>=240)]
	df_full_game_home = df_full_game.loc[(df_full_game['team']==home_team)]
	df_full_game_away = df_full_game.loc[(df_full_game['team']==away_team)]
	feature = st.selectbox('Check out frequency of individual statistics:', df_full_game.columns.drop(['team', 'mp', 'fg_pct', 'fg3_pct', 'ft_pct', 'quarter']))

	new_df = df_full_game_home[feature]
	fig2 = px.histogram(new_df, x=feature, title=(home_team.upper()+" Frequency"))
	st.plotly_chart(fig2)

	new_df1 = df_full_game_away[feature]
	fig3 = px.histogram(new_df1, x=feature, title=(away_team.upper()+" Frequency"))
	st.plotly_chart(fig3)

	

else:
	st.write('Please choose a matchup')

#st.write(df)



df = pd.read_csv('current_nba_data.csv')


df_matchups = pd.concat([df['team'], df['away_team_x']], axis=1)
df_matchups.columns = ['home_team', 'away_team']


df_matchup_merge = pd.merge(df_matchups, df_team, how='left', left_on=['home_team'], right_on=['teams'])


if st.checkbox('Check out all data from the current 2020 season'): 
     st.write(df)

#st.table(df)


# stats = st.multiselect('Show shit per team?', df.columns)
# home_team = st.selectbox('Home Team', df['home_team'].unique())
# away_team = st.selectbox('Away Team', df['away_team'].unique())
# new_df = df.loc[(df['home_team']==home_team) | (df['home_team']==away_team) | (df['away_team']==home_team) | (df['away_team']==away_team)]
# st.write(new_df)
# fig = px.scatter(df, x=(df['home_team']==home_team), y=(df['away_team']==away_team), color=new_df[stats])
# st.plotly_chart(fig)



# species = st.multiselect('What teams do you want to compare', df['home_team'].unique())
# #col1 = st.selectbox('Which feature on x?', df.columns[0:20])
# #col2 = st.selectbox('Which feature on y?', df.columns[0:20])

# if len(species) == 0:
# 	st.write('Select a team')
# elif len(species) == 1:
# 	new_df = df[(df['home_team'].isin(species))]

# 	avgs = new_df.mean()
# 	st.write(avgs)

# 	st.write(new_df)
# 	#fig = px.scatter(new_df, x =col1,y=col2, color='home_team')
# 	#st.plotly_chart(fig)


# 	feature = st.selectbox('Which feature?', df.columns[0:20])
# 	# Filter dataframe
# 	new_df2 = df[(df['home_team'].isin(species))][feature]
# 	fig2 = px.histogram(new_df, x=feature, color="home_team", marginal="rug")
# 	st.plotly_chart(fig2)


# 	fig = px.scatter(new_df, x =feature, y=df[(df['home_team'].isin(species))]['date'] ,color='home_team')
# 	st.plotly_chart(fig)

# else:
# 	st.write('one sec')



st.sidebar.write("""
•	2P - 2-Point Field Goals

•	2P% - 2-Point Field Goal Percentage; the formula is 2P / 2PA.

•	2PA - 2-Point Field Goal Attempts

•	3P - 3-Point Field Goals (available since the 1979-80 season in the NBA)

•	3P% - 3-Point Field Goal Percentage (available since the 1979-80 season in the NBA); the formula is 3P / 3PA.

•	3PA - 3-Point Field Goal Attempts (available since the 1979-80 season in the NBA)

•	Age - Age; player age on February 1 of the given season.

•	AST - Assists

•	AST% - Assist Percentage (available since the 1964-65 season in the NBA); the formula is 100 * AST / (((MP / (Tm MP / 5)) * Tm FG) - FG). Assist percentage is an estimate of the percentage of teammate field goals a player assisted while he was on the floor.

•	Award Share - The formula is (award points) / (maximum number of award points). For example, in the 2002-03 MVP voting Tim Duncan had 962 points out of a possible 1190. His MVP award share is 962 / 1190 = 0.81.

•	BLK - Blocks (available since the 1973-74 season in the NBA)

•	BLK% - Block Percentage (available since the 1973-74 season in the NBA); the formula is 100 * (BLK * (Tm MP / 5)) / (MP * (Opp FGA - Opp 3PA)). Block percentage is an estimate of the percentage of opponent two-point field goal attempts blocked by the player while he was on the floor.

•	BPM - Box Plus/Minus (available since the 1973-74 season in the NBA); a box score estimate of the points per 100 possessions that a player contributed above a league-average player, translated to an average team. Please see the article About Box Plus/Minus (BPM) for more information.

•	DPOY - Defensive Player of the Year

•	DRB - Defensive Rebounds (available since the 1973-74 season in the NBA)

•	DRB% - Defensive Rebound Percentage (available since the 1970-71 season in the NBA); the formula is 100 * (DRB * (Tm MP / 5)) / (MP * (Tm DRB + Opp ORB)). Defensive rebound percentage is an estimate of the percentage of available defensive rebounds a player grabbed while he was on the floor.

•	DRtg - Defensive Rating (available since the 1973-74 season in the NBA); for players and teams it is points allowed per 100 posessions. This rating was developed by Dean Oliver, author of Basketball on Paper. Please see the article Calculating Individual Offensive and Defensive Ratings for more information.

•	DWS - Defensive Win Shares; please see the article Calculating Win Shares for more information.

•	eFG% - Effective Field Goal Percentage; the formula is (FG + 0.5 * 3P) / FGA. This statistic adjusts for the fact that a 3-point field goal is worth one more point than a 2-point field goal. For example, suppose Player A goes 4 for 10 with 2 threes, while Player B goes 5 for 10 with 0 threes. Each player would have 10 points from field goals, and thus would have the same effective field goal percentage (50%).

•	FG - Field Goals (includes both 2-point field goals and 3-point field goals)

•	FG% - Field Goal Percentage; the formula is FG / FGA.

•	FGA - Field Goal Attempts (includes both 2-point field goal attempts and 3-point field goal attempts)

•	FT - Free Throws

•	FT% - Free Throw Percentage; the formula is FT / FTA.

•	FTA - Free Throw Attempts

•	Four Factors - Dean Oliver's "Four Factors of Basketball Success"; please see the article Four Factors for more information.

•	G - Games

•	GB - Games Behind; the formula is ((first W - W) + (L - first L)) / 2, where first W and first L stand for wins and losses by the first place team, respectively.

•	GmSc - Game Score; the formula is PTS + 0.4 * FG - 0.7 * FGA - 0.4*(FTA - FT) + 0.7 * ORB + 0.3 * DRB + STL + 0.7 * AST + 0.7 * BLK - 0.4 * PF - TOV. Game Score was created by John Hollinger to give a rough measure of a player's productivity for a single game. The scale is similar to that of points scored, (40 is an outstanding performance, 10 is an average performance, etc.).

•	GS - Games Started (available since the 1982 season)

•	L - Losses

•	L Pyth - Pythagorean Losses; the formula is G - W Pyth.

•	Lg - League

•	MVP - Most Valuable Player

•	MP - Minutes Played (available since the 1951-52 season)

•	MOV - Margin of Victory; the formula is PTS - Opp PTS.

•	ORtg - Offensive Rating (available since the 1977-78 season in the NBA); for players it is points produced per 100 posessions, while for teams it is points scored per 100 possessions. This rating was developed by Dean Oliver, author of Basketball on Paper. Please see the article Calculating Individual Offensive and Defensive Ratings for more information.

•	Opp - Opponent

•	ORB - Offensive Rebounds (available since the 1973-74 season in the NBA)

•	ORB% - Offensive Rebound Percentage (available since the 1970-71 season in the NBA); the formula is 100 * (ORB * (Tm MP / 5)) / (MP * (Tm ORB + Opp DRB)). Offensive rebound percentage is an estimate of the percentage of available offensive rebounds a player grabbed while he was on the floor.

•	OWS - Offensive Win Shares; please see the article Calculating Win Shares for more information.

•	Pace - Pace Factor (available since the 1973-74 season in the NBA); the formula is 48 * ((Tm Poss + Opp Poss) / (2 * (Tm MP / 5))). Pace factor is an estimate of the number of possessions per 48 minutes by a team. (Note: 40 minutes is used in the calculation for the WNBA.)

•	PER - Player Efficiency Rating (available since the 1951-52 season); PER is a rating developed by ESPN.com columnist John Hollinger. In John's words, "The PER sums up all a player's positive accomplishments, subtracts the negative accomplishments, and returns a per-minute rating of a player's performance." Please see the article Calculating PER for more information.

•	Per 36 Minutes - A statistic (e.g., assists) divided by minutes played, multiplied by 36.

•	Per Game - A statistic (e.g., assists) divided by games.

•	PF - Personal Fouls

•	Poss - Possessions (available since the 1973-74 season in the NBA); the formula for teams is 0.5 * ((Tm FGA + 0.4 * Tm FTA - 1.07 * (Tm ORB / (Tm ORB + Opp DRB)) * (Tm FGA - Tm FG) + Tm TOV) + (Opp FGA + 0.4 * Opp FTA - 1.07 * (Opp ORB / (Opp ORB + Tm DRB)) * (Opp FGA - Opp FG) + Opp TOV)). This formula estimates possessions based on both the team's statistics and their opponent's statistics, then averages them to provide a more stable estimate. Please see the article Calculating Individual Offensive and Defensive Ratings for more information.

•	PProd - Points Produced; Dean Oliver's measure of offensive points produced. Please see the article Calculating Individual Offensive and Defensive Ratings for more information.

•	PTS - Points

•	ROY - Rookie of the Year

•	SMOY - Sixth Man of the Year

•	SOS - Strength of Schedule; a rating of strength of schedule. The rating is denominated in points above/below average, where zero is average. My colleague Doug Drinen of Pro-Football-Reference.com has written a great explanation of this method.

•	SRS - Simple Rating System; a rating that takes into account average point differential and strength of schedule. The rating is denominated in points above/below average, where zero is average. My colleague Doug Drinen of Pro-Football-Reference.com has written a great explanation of this method.

•	STL - Steals (available since the 1973-74 season in the NBA)

•	STL% - Steal Percentage (available since the 1973-74 season in the NBA); the formula is 100 * (STL * (Tm MP / 5)) / (MP * Opp Poss). Steal Percentage is an estimate of the percentage of opponent possessions that end with a steal by the player while he was on the floor.

•	Stops - Stops; Dean Oliver's measure of individual defensive stops. Please see the article Calculating Individual Offensive and Defensive Ratings for more information.

•	Tm - Team

•	TOV - Turnovers (available since the 1977-78 season in the NBA)

•	TOV% - Turnover Percentage (available since the 1977-78 season in the NBA); the formula is 100 * TOV / (FGA + 0.44 * FTA + TOV). Turnover percentage is an estimate of turnovers per 100 plays.

•	TRB - Total Rebounds (available since the 1950-51 season)

•	TRB% - Total Rebound Percentage (available since the 1970-71 season in the NBA); the formula is 100 * (TRB * (Tm MP / 5)) / (MP * (Tm TRB + Opp TRB)). Total rebound percentage is an estimate of the percentage of available rebounds a player grabbed while he was on the floor.

•	TS% - True Shooting Percentage; the formula is PTS / (2 * TSA). True shooting percentage is a measure of shooting efficiency that takes into account field goals, 3-point field goals, and free throws.

•	TSA - True Shooting Attempts; the formula is FGA + 0.44 * FTA.

•	Usg% - Usage Percentage (available since the 1977-78 season in the NBA); the formula is 100 * ((FGA + 0.44 * FTA + TOV) * (Tm MP / 5)) / (MP * (Tm FGA + 0.44 * Tm FTA + Tm TOV)). Usage percentage is an estimate of the percentage of team plays used by a player while he was on the floor.

•	VORP - Value Over Replacement Player (available since the 1973-74 season in the NBA); a box score estimate of the points per 100 TEAM possessions that a player contributed above a replacement-level (-2.0) player, translated to an average team and prorated to an 82-game season. Multiply by 2.70 to convert to wins over replacement. Please see the article About Box Plus/Minus (BPM) for more information.

•	W - Wins

•	W Pyth - Pythagorean Wins; the formula is G * (Tm PTS14 / (Tm PTS14 + Opp PTS14)). The formula was obtained by fitting a logistic regression model with log(Tm PTS / Opp PTS) as the explanatory variable. Using this formula for all BAA, NBA, and ABA seasons, the root mean-square error (rmse) is 3.14 wins. Using an exponent of 16.5 (a common choice), the rmse is 3.48 wins. (Note: An exponent of 10 is used for the WNBA.)

•	W-L% - Won-Lost Percentage; the formula is W / (W + L).

•	WS - Win Shares; an estimate of the number of wins contributed by a player. Please see the article Calculating Win Shares for more information.

•	WS/48 - Win Shares Per 48 Minutes (available since the 1951-52 season in the NBA); an estimate of the number of wins contributed by the player per 48 minutes (league average is approximately 0.100). Please see the article Calculating Win Shares for more information.

•	Win Probability - The estimated probability that Team A will defeat Team B in a given matchup.

•	Year - Year that the season occurred. Since the NBA season is split over two calendar years, the year given is the last year for that season. For example, the year for the 1999-00 season would be 2000.


	""")


	









# sidebar example
# teams = df['home_team'].drop_duplicates()
# st.sidebar.header('Features')
# home_team = st.sidebar.selectbox('Choose home team', teams)

# st.write(home_team)

# away_team = st.sidebar.selectbox('Choose away team', teams)

# st.write(away_team)
