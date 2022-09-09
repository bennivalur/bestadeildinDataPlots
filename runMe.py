import pandas as pd
import matplotlib.pyplot as plt
import os
import urllib.request
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
import json
import statistics

#xG,passes,
metric = 'xG'

#Key is team name in .csv
#Value is prefix of .png image
team_pics = {
    "Víkingur R.":"VÍKR",
    "Valur":"Valur",
    "Stjarnan":"STJA",
    "Breiðablik":"BREI",
    "KA":"KA",
    "FH":"FH",
    "ÍA":"IA",
    "Keflavík":"KEF",
    "Leiknir R.":"LEI",
    "KR":"KR",
    "Afturelding":"AFT",
    "Þróttur R.":"ÞRO",
    "Þór/KA":"ÞORKA",
    "Selfoss":"SEL",
    "ÍBV":"IBV",
    "Fram":"FRA"
}

def getImage(path): 
    return OffsetImage(plt.imread(path), zoom=.5)

def calcMetric(team,games,metric,isPerGame):
    metricValue = 0
    metricAgaintsValue = 0
    for g in games:
        if(g['Heimalið'] == team):
            metricValue += g['h_'+metric]
            metricAgaintsValue += g['a_'+metric]
        else:
            metricValue += g['a_'+metric]
            metricAgaintsValue += g['h_'+metric]

    if isPerGame:
        metricValue = metricValue / len(games)
        metricAgaintsValue = metricAgaintsValue / len(games)

    return {metric:round(metricValue,2),metric+'Against':round(metricAgaintsValue,2)}



cs = pd.read_csv('data/BestaStats-Karla.csv')
cs.to_json('data/BestaStats-Karla.json',orient='records')

with open('data/BestaStats-Karla.json','r') as main_stats:
    data = json.load(main_stats)

teams = []
games = []
for d in data:
    if d['Heimalið'] not in teams:
        teams.append(d['Heimalið'])
    if d['h_mörk'] != None:
        games.append(d)


teamGames = {}
logoList = []
x = []
y = []
for t in teams:
    teamGames[t] = list(filter(lambda x: x['Heimalið'] == t or x['Útilið'] == t,games))

    teamGames[t] = calcMetric(t,teamGames[t],metric,True)

    logoList.append(team_pics[t]+'.png')
    y.append(teamGames[t][metric])
    x.append(teamGames[t][metric+'Against'])




logos = os.listdir(os.getcwd() + '/logos')

logo_paths = []

for i in logoList:
    logo_paths.append(os.getcwd() + '/logos/' + str(i))


fig, ax = plt.subplots()

#Make a scatter plot first to get the points to place logos
ax.scatter(x, y, s=.001)
ax.invert_xaxis()

#Adding logos to the chart
for x0, y0, path in zip(x, y, logo_paths):
    ab = AnnotationBbox(getImage(path), (x0, y0), frameon=False, fontsize=4)
    ax.add_artist(ab)

#Adding labels and text
ax.set_xlabel(metric+' Against', fontsize=16)
ax.set_ylabel(metric, fontsize=16)

#Add a grid
ax.grid(zorder=0,alpha=.4)
ax.set_axisbelow(True)

#ax.invert_xaxis()

ax.set_title('Data provided by @bestadeildin as of ' + games[-1]['Leikdagur'], fontsize=7)
plt.suptitle('Bestadeildin 2022 ' + metric + ' Vs. ' + metric  + 'Against', fontsize=18)
plt.figtext(.66, .02, 'Data: @bestadeildin | Graph: @bennivaluR_', fontsize=7)
#plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)), 
#        color='darkorange', linestyle='--')
plt.plot([statistics.mean(x),statistics.mean(x)],[max(y),min(y)], 
        color='darkorange', linestyle='--')
plt.plot([max(x),min(x)],[statistics.mean(y),statistics.mean(y)], 
        color='darkorange', linestyle='--')

#Create directory if it does not exist
"""
try: 
    os.makedirs('graphs')
except OSError:
    if not os.path.isdir('graphs'):
        raise
"""
#Save the figure as a png
plt.savefig('graphs/besta' + metric + 'vs' + metric + 'A.png', dpi=400)