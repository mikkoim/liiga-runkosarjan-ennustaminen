# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 16:54:19 2017

@author: Mikko
"""

import urllib.request as urllib
from bs4 import BeautifulSoup
url = "http://liiga.fi/ottelut/2017-2018/runkosarja/1/kokoonpanot/"

def game_players(url):
    page = urllib.urlopen(url)
    
    soup = BeautifulSoup(page, "html.parser")
    
    h2 = soup.find_all("a", class_="player")
    
    [home_name, away_name] = soup.find_all("span", class_="team-name")
    home_name = home_name.get_text().strip()
    away_name = away_name.get_text().strip()

    score = soup.find_all("p", class_="score")
    score = score[0].get_text().strip()
    score_h = score[0]
    score_a = score[-1]
    
    tab = []
    for i in h2:
    
        playername = i.find_all("div", class_="name")[0]
    
        strin = playername.get_text().strip()
        tab.append(strin)
        
    home = tab[0:21]
    away = tab[21:42]
    tab = [[home_name, score_h, home], [away_name, score_a, away]]
    return tab

games = []
#1,229
#2016-2017 runko
#4147,4596

#2015-2016
#7612,8061

#2014-2015
#6130,6535
i = 1
for id in range(1,229):

    url = "http://liiga.fi/ottelut/2017-2018/runkosarja/" + str(id) + "/kokoonpanot/"
    tab = game_players(url)
    games.append(tab) 
    print(str(i) + "/450")
    i = i+1

