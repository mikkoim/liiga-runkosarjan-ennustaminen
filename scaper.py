# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 16:54:19 2017

@author: Mikko Impiö

Sisältää game_players- funktion sekä skriptin SM-Liigan ottelukohtaisten
pelaajakokoonpanojen ja tuloksien raapimiseen SM-Liigan tilastosivuilta.
"""

import urllib.request as urllib
from bs4 import BeautifulSoup
"""
Funktio hakee tietyltä ottelukokoonpanosivulta pelaajakokoonpanot ja ottelun
tulokset, ja palauttaa nämä taulukossa muodossa:
    
0.Kotijoukkueen tiedot(array)
    0.0.Kotijoukkueen nimi(string)
    0.1.Kotijoukkueen maalit(int)
    0.2.Kotijoukkueen pelaajat(array)
        0.2.0.Pelaaja1
        ...
        0.2.20.Pelaaja21
1.Vierasjoukkueen tiedot(array)
    1.0.Vierasjoukkueen nimi(string)
    1.1.Vierasjoukkueen maalit(int)
    1.2.Vierasjoukkueen pelaajat(array)
        1.2.0.Pelaaja1
        ...
        1.2.20.Pelaaja21
2.Tieto jatkoajasta(boolean)
     
"""
def game_players(url):
    page = urllib.urlopen(url)
    
    soup = BeautifulSoup(page, "html.parser")
    
    #Pelaajat
    h2 = soup.find_all("a", class_="player")
    
    #Joukkueiden nimet
    [home_name, away_name] = soup.find_all("span", class_="team-name")
    home_name = home_name.get_text().strip()
    away_name = away_name.get_text().strip()

    #Tulokset
    score = soup.find_all("p", class_="score")
    score = score[0].get_text().strip()
    score_h = score[0]
    score_a = score[-1]

    #Tieto jatkoajasta
    status = soup.find_all("p", class_="status")[0]
    status = status.get_text()
    if ("(JA)" or "(VL)") in status:
        jatko = True
    else: 
        jatko = False

    #Pelaajien nimet
    tab = []
    for i in h2:
    
        playername = i.find_all("div", class_="name")[0]
    
        strin = playername.get_text().strip()
        tab.append(strin)
        
    home = tab[0:21]
    away = tab[21:42]

    #Kootaan tiedot yhteen
    tab = [[home_name, score_h, home], [away_name, score_a, away], jatko]
    return tab

games = []

#Alla liigan verkkosivujen indeksit tiettyjen kausien pelien kokoonpanosivuille
#2017-2018
#1,229

#2016-2017
#4147,4596

#2015-2016
#7612,8061

#2014-2015
#6130,6535
i = 1
for id in range(6130,6535):

    url = "http://liiga.fi/ottelut/2014-2015/runkosarja/" + str(id) + "/kokoonpanot/"
    tab = game_players(url)
    games.append(tab) 
    print(str(i) + "/450")
    i = i+1

