# -*- coding: utf-8 -*-
"""recommender2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18PixEyOMVJ0LrRJ8YbJWtJXnmhBrvRp0
"""

import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
import streamlit as st

data = pd.read_csv('skaters.csv')

st.title('NHL Player Recommender')
st.write("This system uses advanced statistics to indentify similarity between players. This model predicts based on the proprotion of different ways that players add value to their team. For example if you type in Connor McDavid you aren't going to get Sidney Crosby, because they produce in different ways for their team. Type a player's first and last name in the text box with a space seperating them, and then hit enter. (Note: this application only uses players from the 2021-2022 season that appeared in 50 or more games.)")
playerName = st.text_input('Enter player name:', 'Artemi Panarin')

for col in data.columns:
    print(col)

data1 = data.loc[data['situation']=='all']

data2 = data1.loc[data['games_played']>= 50]

twoD = data2.loc[:,["name",'team','iceTimeRank','position','icetime','I_F_points','I_F_xGoals','I_F_shotsOnGoal',"OnIce_F_xGoals","OnIce_A_xGoals",'I_F_hits','I_F_takeaways','I_F_giveaways','penalityMinutes','penalityMinutesDrawn','shotsBlockedByPlayer']]

twoD['per60'] = twoD['icetime']/3600

twoD['xG/60'] = twoD["OnIce_F_xGoals"]/twoD['per60']

twoD['xGA/60'] = twoD["OnIce_A_xGoals"]/twoD['per60']

twoD['error'] = twoD["xG/60"]-twoD['xGA/60']

xGoalBins = [-np.inf,-1,0,1,np.inf]
group_names=['bad','good','great','elite']
twoD['xGoalBins']=pd.cut(twoD['error'],xGoalBins,labels=group_names)

icetimeBins = [0,23930,47860,71790,np.inf]
group_names=['low','medium','strong','heavy']
twoD['icetimeBins']=pd.cut(twoD['icetime'],icetimeBins,labels=group_names)

twoD['I_F_shotsOnGoal'].median()

twoD['I_F_shotsOnGoal'].max()

sogBins = [0,36,72,108,np.inf]
group_names=['never','quality','quantity','high']
twoD['sogBins']=pd.cut(twoD['I_F_shotsOnGoal'],sogBins,labels=group_names)

twoD['I_F_hits'].median()

twoD['I_F_hits'].max()

hitBins = [0,23,46,69,np.inf]
group_names=['soft','even','physical','hitter']
twoD['hitBins']=pd.cut(twoD['I_F_hits'],hitBins,labels=group_names)

twoD['penalityMinutes'].median()

penBins = [0,13,26,39,np.inf]
group_names=['baby','somewhat','dirty','goon']
twoD['penBins']=pd.cut(twoD['penalityMinutes'],penBins,labels=group_names)

twoD['shotsBlockedByPlayer'].median()

blockedBins = [0,21,42,63,np.inf]
group_names=['wimp','skillguy','ferda','beast']
twoD['blockBins']=pd.cut(twoD['shotsBlockedByPlayer'],blockedBins,labels=group_names)

twoD['I_F_takeaways'].median()

takeawayBins = [0,13,27,41,np.inf]
group_names=['nostick','decent','smart','sticky']
twoD['takeawayBins']=pd.cut(twoD['I_F_takeaways'],takeawayBins,labels=group_names)

twoD['I_F_points'].median()

pointBins = [0,30,60,90,np.inf]
group_names=['nobody','middle','sick','nasty']
twoD['pointBins']=pd.cut(twoD['I_F_points'],pointBins,labels=group_names)

twoD["combined"] = twoD["position"] + ' ' + twoD["icetimeBins"].astype(str) + ' ' + twoD['xGoalBins'].astype(str) + ' ' + twoD['sogBins'].astype(str) + ' ' + twoD['hitBins'].astype(str) + ' ' + twoD['penBins'].astype(str) + ' ' + twoD['blockBins'].astype(str) + ' ' + twoD['takeawayBins'].astype(str) + ' ' + twoD['pointBins'].astype(str)

twoD = twoD.reset_index(drop=True)

twoD["PlayerId"] = twoD.index

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

cm = CountVectorizer().fit_transform(twoD['combined'])

cs = cosine_similarity(cm)
print(cs)

player_Id = twoD[twoD.name == playerName]['PlayerId'].values[0]

scores = list(enumerate(cs[player_Id]))
print(scores)

sorted_scores = sorted(scores,key=lambda x:x[1], reverse=True)
sorted_scores = sorted_scores[0:]
print(sorted_scores)

j = 0
st.write('Most similar player to '+playerName+' is . . .')
for item in sorted_scores:
  recommendedPlayer = twoD[twoD.PlayerId == item[0]]['name'].values[0]
  j=j+1
  if item[0] == player_Id:
    continue
  st.write(recommendedPlayer)
  if j >= 1:
    break

playerDf = twoD.loc[twoD['name']==recommendedPlayer]
playerDf = playerDf.reset_index(drop=True)
playerDf = playerDf.loc[:,['name','team','position','I_F_points',"I_F_xGoals","OnIce_F_xGoals","OnIce_A_xGoals",'I_F_shotsOnGoal','I_F_hits','shotsBlockedByPlayer','I_F_takeaways','penalityMinutes']]

playerNameDf = twoD.loc[twoD['name']==playerName]
playerNameDf = playerNameDf.reset_index(drop=True)
playerNameDf = playerNameDf.loc[:,['name','team','position','I_F_points',"I_F_xGoals","OnIce_F_xGoals","OnIce_A_xGoals",'I_F_shotsOnGoal','I_F_hits','shotsBlockedByPlayer','I_F_takeaways','penalityMinutes']]

st.dataframe(playerNameDf)

playerDf

x = np.linspace(0,180,180)
y = x

plt_1 = plt.figure(figsize=(8, 8))
plt.scatter(playerDf['OnIce_F_xGoals'],playerDf["OnIce_A_xGoals"],color = 'red')
plt.scatter(playerNameDf['OnIce_F_xGoals'],playerNameDf["OnIce_A_xGoals"],color = 'blue')
plt.plot(x,y,'--', color = 'black')

plt.xlim([0,180])
plt.ylim([0,180])
plt.legend([playerDf['name'][0],playerNameDf['name'][0],'even'])
plt.xlabel("On Ice Expected Goals For")
plt.ylabel("On Ice Expected Goals Against")

st.write(plt_1)

j = 0
st.write('Top 5 most similar players to '+playerName+' :')
for item in sorted_scores:
  recommendedPlayer = twoD[twoD.PlayerId == item[0]]['name'].values[0]
  j=j+1
  if item[0] == player_Id:
    continue
  st.write(recommendedPlayer)
  if j >= 6:
    break