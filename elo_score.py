# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 20:13:25 2017

@author: Mikko




Pelaaja-luokka sisältää yksittäisen pelaajan tiedot:
    Nimen ja ELO-luvun
"""
class Pelaaja:

    def __init__(self, nimi, ELO):
        self.__nimi = nimi
        self.__elo = ELO
    def updateELO(self, ELO):
        self.__elo = ELO
    def getNimi(self):
        return self.__nimi
    def getELO(self):
        return self.__elo
"""
Players on lista pelaajista, listasta on mahdollista hakea
ELO-lukujen keskiarvot, pelaajien nimet, pelaajaoliot sekä ELO-luvut
Lista on myös mahdollista järjestää ELO-luvun perusteella
"""       
class Players:

    def __init__(self):
        self.__playerlist = []
        self.__playernames = []
        self.__length = 0
        
    def getPlayers(self):
        return self.__playerlist
    
    def getNames(self):
        return self.__playernames
    
    def getELOs(self):
        ELOs = []
        for player in self.__playerlist:
            ELOs.append(player.getELO())
        return ELOs
    
    def ELOmean(self):
        ELO_sum = 0
        for player in self.__playerlist:
            ELO = player.getELO()
            ELO_sum = ELO_sum + ELO
        return ELO_sum/len(self.__playerlist)
    
    def playerELO(self, player_name):
        for player in self.__playerlist:
            if player.getNimi() == player_name:
                return player.getELO()
    
    def addPlayer(self, Pelaaja):
        self.__playerlist.append(Pelaaja)
        self.__playernames.append(Pelaaja.getNimi())
        
    def changeELO(self, ELO_change):
        for player in self.__playerlist:
            orig_ELO = player.getELO()
            player.updateELO(orig_ELO + ELO_change)
            
    def resetELO(self, ELO=1500):
        for player in self.__playerlist:
            player.updateELO(ELO)
            
    def getSorted(self, reverse=False):
        sortedPlayers = Players()
        indices = sorted(range(len(self.getELOs())),key=lambda x:self.getELOs()[x], reverse = reverse)
        for i in indices:
            sortedPlayers.addPlayer(self.__playerlist[i])
        return sortedPlayers
            
"""
Järjestää dictionaryn arvon perusteella ja tulostaa sen
ensimmäisen kuuden jälkeen viivat erottelua varten (6 parasta)
"""
def sorted_dict(dictionary, reverse = True):

    scores = []
    for joukkue in dictionary:
        scores.append(dictionary[joukkue])
        
    indices = sorted(range(len(scores)),key=lambda x:scores[x], reverse = reverse)
    
    for ind, i in enumerate(indices):
        score = scores[i]
        for joukkue, pisteet in dictionary.items():
            if pisteet == score:
                print(joukkue, pisteet)
        if ind == 5:
            print("------")
      
def team_ELOs(game):
    home = Players()
    home_player_names = game[0][2]
    
    #käydään joukkueen pelaajat läpi
    for player_name in home_player_names:
        
        #kerätään pelaajat joukkuekohtaiseen listaan
        for player in p.getPlayers():
            if player.getNimi() == player_name:
                home.addPlayer(player)
                
    #sama vierasjoukkueelle
    away = Players()
    away_player_names = game[1][2]
    for player_name in away_player_names:
        
        #kerätään pelaajat joukkuekohtaiseen listaan
        for player in p.getPlayers():
            if player.getNimi() == player_name:
                away.addPlayer(player)
                
    R_a = home.ELOmean()
    R_b = away.ELOmean()
    
    return home, away, R_a, R_b
#%%
"""
Kohdassa alustetaan pelaajalista p, johon talletetaan pelaajat ja 
ELO-arvot 
"""
kaudet = [kausi1617, kausi1516, kausi1415]
p = Players()

STANDARD_ELO = 1500

for kausi in kaudet:
    for game in kausi:
        for team in game:
            team_players = team[2]
            for player_name in team_players:
                if player_name not in p.getNames():
                    player = Pelaaja(player_name, STANDARD_ELO)
                    p.addPlayer(player)
                    
#%% Tulostaa pelaajalistan ensimmäiset 50 pelaajaa 
#ei-järjestettynä ja järjestettynä
for i in range(0,50):
    print(p.getPlayers()[i].getNimi(), p.getPlayers()[i].getELO())
  
print("\n\n")
s = p.getSorted(reverse = True)
for i in range(0,50):
    print(s.getPlayers()[i].getNimi(), s.getPlayers()[i].getELO())
    
#%% Ajaa kausien ottelut läpi ja muuttaa pelaajalistan p ELO-painotukset
#tämän mukaisesti

def train(p, kaudet, K, printOut = True):
    for kausi in kaudet:
        #käydään pelit läpi
        for ind, game in enumerate(kausi):
           
            #tarkistetaan pelin tulos
            score_home = game[0][1] 
            score_away = game[1][1]
            
            if score_home > score_away:
                S_a = 3
                S_b = 0
            else:
                S_a = 0
                S_b = 3
            #joukkuekohtaiset ELO-luvut ja kokoonpanot
            home, away, R_a, R_b = team_ELOs(game)
            
            #Odotusarvo pisteille
            E_a = 3/(1 + 10**((R_b - R_a)/400))
            E_b = 3/(1 + 10**((R_a - R_b)/400))
            
            #Muutetaan kaikkien joukkueen pelaajien ELO-lukua muutoksen
            #mukaisesti
            ELO_muutos_a = K*(S_a - E_a)
            ELO_muutos_b = K*(S_b - E_b)
            
            home.changeELO(ELO_muutos_a)
            away.changeELO(ELO_muutos_b)
            
            if printOut: print(ind)
            
    return p

kaudet = [kausi1415, kausi1516, kausi1617]
K = 4
p = train(p, kaudet, K)

#%% Ennustaa joukkueiden pisteet kaudella pelaajien ELO-arvojen
#perusteella

def test(p, kausi):
    """tehdään dictionary joukkueista"""
    joukkueet = {}

    for game in kausi:
        for team in game:
            team_name = team[0]
            joukkueet[team_name] = 0
           
    """käydään kauden pelit läpi ja lasketaan niiden odotuspistemäärä"""
    for ind, game in enumerate(kausi):
        #joukkuekohtaiset ELO-luvut ja kokoonpanot
        home, away, R_a, R_b = team_ELOs(game)
        
        #tuloksen odotusarvo
        E_a = 3/(1 + 10**((R_b - R_a)/400))
        E_b = 3/(1 + 10**((R_a - R_b)/400))
        
#        score_home = game[0][1] 
#        score_away = game[1][1]
        
        home_name = game[0][0]
        away_name = game[1][0]

        joukkueet[home_name] = joukkueet[home_name] + E_a
        joukkueet[away_name] = joukkueet[away_name] + E_b

        print(ind)
        
    return joukkueet
    
kausi = kausi1718
joukkueet = test(p, kausi)
#%% Printtaa joukkueet
for i in joukkueet:
    print(i, joukkueet[i])
#%% Joukkueet pistejärjestyksessä
sorted_dict(joukkueet)

#%%
#laskee seuraavan pelin tuloksen, ja korjaa ELO-arvoa tämän jälkeen 
#pelin todellisen tuloksen perusteella
def seuraava_peli(kausi, p):
    oikein = 0
    for i in range(len(kausi)):
        """ennustetaan pelin tulos joukkueiden ELOjen perusteella"""
        game = kausi[i]
        
        score_home = game[0][1] 
        score_away = game[1][1]
        
        home, away, R_a, R_b = team_ELOs(game) 
        
        if (R_a > R_b and score_home > score_away) \
            or (R_a < R_b and score_home < score_away):
            oikein = oikein + 1
            
        """muutetaan pelaajien ELO-lukuja todellisen tuloksen perusteella"""
        kaudet = [ [kausi[i]] ] #vastaa yhtä peliä ainoastaan
        p = train(p, kaudet, K, printOut = False)
        
    acc = oikein/len(kausi)
    return acc

kausi = kausi1718
print(seuraava_peli(kausi, p))

#%%
