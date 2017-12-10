# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 20:13:25 2017

@author: Mikko Impiö

Sisältää luokat pelaajien- ja pelaajalistojen hallintaan ja ELO-lukujen 
kirjanpitoon.
Sisältää myös funktiot ELO-lukujen laskentaan edellisten kausien perusteella, 
sekä kauden pistemäärien ennustamiseen tietyillä pelaajarostereilla.

LUOKAT:
    
    Pelaaja(): sisältää yksittäisen pelaajan tiedot
    
    Players(): lista pelaajista, listasta on mahdollista hakea
            ELO-lukujen keskiarvot, pelaajien nimet, pelaajaoliot 
            sekä ELO-luvut. Lista on myös mahdollista järjestää 
            ELO-luvun perusteella
            
            METODIT:
            getPlayers()
            palauttaa listan pelaajaolioista
            
            getNames()
            palauttaa listan pelaajien nimistä
            
            getELOs()
            palauttaa listan pelaajien ELO-luvuista
            
            ELOmean()
            laskee ja palauttaa pelaajalistassa olevien pelaajien 
            ELO:jen keskiarvot
            
            playerELO(player_name)
            palauttaa tietyn pelaajan ELO-luvun
            
            addPlayer(Pelaaja)
            lisää pelaajaolion pelaajalistaan
            
            changeELO(ELO_change)
            muuttaa KAIKKIEN listassa olevien pelaajien ELO-lukua
            
            resetELO(ELO=1500)
            Nollaa KAIKKIEN listassa olevien pelaajien ELO-luvun 
            valittuun lukuun(oletus 1500)
            
            getSorted(reverse = False)
            Palauttaa pelaajalistan ELO-luvun mukaisessa järjestyksessä
FUNKTIOT:
    
    train(p, kaudet, K, printOut = True)
            Ajaa kausien ottelut läpi ja muuttaa pelaajalistan p ELO-painotukset
            tämän mukaisesti.
            
            p = Players-olio kaikista pelaajista
            kausi = kaudet jolla pelaajien ELO-luku painotetaan
            K = ELO-luvun painotuskerroin
            printOut = tulostetaanko pelin indeksi jossa ollaan menossa
            
    test(p, kausi, seasonELOs = None)
            Ennustaa joukkueiden pisteet kaudella pelaajien ELO-arvojen
            perusteella
            
            p = Players-olio kaikista pelaajista
            kausi = ennustettava kausi ja sen pelit
            seasonELOs = joukkuekohtaiset ELOt lasketaan ennen ennustamista
            seasonELOs jättämällä pois jokaisen ottelun ELO lasketaan erikseen
            riippuen peliin osallistuvista pelaajista
            
    seuraava_peli(kausi, p)
            laskee seuraavan pelin tuloksen, ja korjaa ELO-arvoa tämän jälkeen 
            pelin todellisen tuloksen perusteella
            
            p = Players-olio kaikista pelaajista
            kausi = kausi, jota ollaan ennustamassa
    
!! Ohjelma olettaa, että pelitiedot sisältävät muuttujat 
kausi1415, kausi1516, kausi1617 ja kausi1718 
on luotu edellisten scraper.py- skriptin avulla
!!

"""



"""
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
            
    #palauttaa listan pelaajaolioista
    def getPlayers(self):
        return self.__playerlist
        
    #palauttaa listan pelaajien nimistä
    def getNames(self):
        return self.__playernames
    
    #palauttaa listan pelaajien ELO-luvuista
    def getELOs(self):
        ELOs = []
        for player in self.__playerlist:
            ELOs.append(player.getELO())
        return ELOs
    
    #laskee ja palauttaa pelaajalistassa olevien pelaajien ELO:jen keskiarvot
    def ELOmean(self):
        ELO_sum = 0
        for player in self.__playerlist:
            ELO = player.getELO()
            ELO_sum = ELO_sum + ELO
        return ELO_sum/len(self.__playerlist)
    
    #palauttaa tietyn pelaajan ELO-luvun
    def playerELO(self, player_name):
        for player in self.__playerlist:
            if player.getNimi() == player_name:
                return player.getELO()
    
    #lisää pelaajaolion pelaajalistaan
    def addPlayer(self, Pelaaja):
        self.__playerlist.append(Pelaaja)
        self.__playernames.append(Pelaaja.getNimi())
        
    #muuttaa KAIKKIEN listassa olevien pelaajien ELO-lukua
    def changeELO(self, ELO_change):
        for player in self.__playerlist:
            orig_ELO = player.getELO()
            player.updateELO(orig_ELO + ELO_change)
            
    #Nollaa KAIKKIEN listassa olevien pelaajien ELO-luvun valittuun lukuun
    def resetELO(self, ELO=1500):
        for player in self.__playerlist:
            player.updateELO(ELO)
            
    #Palauttaa pelaajalistan ELO-luvun mukaisessa järjestyksessä
    def getSorted(self, reverse=False):
        sortedPlayers = Players()
        indices = sorted(range(len(self.getELOs())),key=lambda x:self.getELOs()[x], reverse = reverse)
        for i in indices:
            sortedPlayers.addPlayer(self.__playerlist[i])
        return sortedPlayers
   

#### APUFUNKTIOT #####         
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
                print("{:} {:.2f}".format(joukkue, pisteet))
        if ind == 5:
            print("------")
      
"""
Kerää tietyn pelin pelaajat ja laskee näiden perusteella ELO-luvun koko
joukkueelle. Palauttaa listat koti- ja vierasjoukkueesta, sekä näiden
ELO-keskiarvot
"""
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
                
    #ELO-keskiarvot
    R_a = home.ELOmean()
    R_b = away.ELOmean()
    
    return home, away, R_a, R_b
    
"""
Laskee jokaiselle kaudella pelaavalle joukkueelle ELO-luvun sen perusteella,
ketä joukkueessa tulee pelaamaan tällä kaudella. Käytetään mallissa, sillä
ei voida tietää ennen kauden alkua varmoja kokoonpanoja otteluille
"""
def team_season_ELOs(kausi, p):
    #Tehdään lista joukkueista
    joukkueet = {}

    for game in kausi:
        for team in game[0:1]:
            team_name = team[0]
            joukkueet[team_name] = Players()
    
    #Käydään pelit läpi
    for game in kausi:
        for team in game[0:1]:
            
            team_name = team[0]

            #Käydään pelaajien nimet läpi joukkueittain, ja lisätään ne
            #joukkueen Players-olioon, jos ko. pelaajaa ei siinä jo ole
            team_player_names = team[2]
            for player_name in team_player_names:
                if player_name not in joukkueet[team_name].getNames():
                    team_players = joukkueet[team_name]

                    for player in p.getPlayers():
                        if player.getNimi() == player_name:
                            team_players.addPlayer(player)
                    
    #Käydään vielä joukkuet läpi ja lasketaan ELO-keskiarvot
    for joukkue in joukkueet.keys():
        joukkueet[joukkue] = joukkueet[joukkue].ELOmean()
        
    return joukkueet
        
    
"""
Luo joukkueet- dictionaryn kaudella pelaavista joukkueista
"""
def alusta_joukkueet(kausi):
    joukkueet = {}

    for game in kausi:
        for team in game[0:1]:
            team_name = team[0]
            joukkueet[team_name] = 0

    return joukkueet
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
        for team in game[0:1]:
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

#p = Players-olio kaikista pelaajista
#K = ELO-luvun painotuskerroin
#printOut = tulostetaanko pelin indeksi jossa ollaan menossa

#palauttaa Players-olion p uusilla ELO-arvoilla
def train(p, kaudet, K, printOut = True):
    for kausi in kaudet:
        #käydään pelit läpi
        for ind, game in enumerate(kausi):
           
            #tarkistetaan pelin tulos
            score_home = game[0][1] 
            score_away = game[1][1]
            
            isJatko = game[2]

            if score_home > score_away:
                if isJatko:
                    S_a = 2
                    S_b = 1
                else:
                    S_a = 3
                    S_b = 0
            else:
                if isJatko:
                    S_a = 1
                    S_b = 2
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

#********** TRAIN **********************************************
#Määritä kaudet joilla ELO-luku lasketaan, painotuskerroin, 
#sekä se, resetoidaanko pelaajalista arvoon 1500 ennen opetusta
#***************************************************************
kaudet = [kausi1415, kausi1516]
K = 4
p.resetELO()
p = train(p, kaudet, K)

#%% Ennustaa joukkueiden pisteet kaudella pelaajien ELO-arvojen
#perusteella

def test(p, kausi, seasonELOs = None):
    #tehdään dictionary joukkueista
    joukkueet = alusta_joukkueet(kausi)
           
    #käydään kauden pelit läpi ja lasketaan niiden odotuspistemäärä
    for ind, game in enumerate(kausi):
        home_name = game[0][0]
        away_name = game[1][0]

        #joukkuekohtaiset ELO-luvut ja kokoonpanot
        if seasonELOs == None:
            home, away, R_a, R_b = team_ELOs(game)
        else:
            R_a = seasonELOs[home_name]
            R_b = seasonELOs[away_name]
            
        
        #tuloksen odotusarvo
        E_a = 3/(1 + 10**((R_b - R_a)/400))
        E_b = 3/(1 + 10**((R_a - R_b)/400))
        


        joukkueet[home_name] = joukkueet[home_name] + E_a
        joukkueet[away_name] = joukkueet[away_name] + E_b

        print(ind)
        
    return joukkueet
    
    
#************* TEST ***********************************************
#Määritä ennustettava kausi, sekä ennusteessa käytettävä ELO-tyyppi
#seasonELOs = joukkuekohtaiset ELOt lasketaan ennen ennustamista
#seasonELOs jättämällä pois jokaisen ottelun ELO lasketaan erikseen
#******************************************************************
kausi = kausi1617
seasonELOs = team_season_ELOs(kausi, p)
joukkueet = test(p, kausi, seasonELOs)

#%% Joukkueet pistejärjestyksessä
sorted_dict(joukkueet)

#%%
#laskee seuraavan pelin tuloksen, ja korjaa ELO-arvoa tämän jälkeen 
#pelin todellisen tuloksen perusteella
#Antaa parhaita tuloksia, koska ennustus on vain yhden ottelun päähän
def seuraava_peli(kausi, p):
    
    #tehdään dictionary joukkueista
    joukkueet = alusta_joukkueet(kausi)

    oikein = 0
    for i in range(len(kausi)):


        #ennustetaan pelin tulos joukkueiden ELOjen perusteella
        game = kausi[i]
        
        score_home = game[0][1] 
        score_away = game[1][1]
        
        home, away, R_a, R_b = team_ELOs(game) 
        
        if (R_a > R_b and score_home > score_away) \
            or (R_a < R_b and score_home < score_away):
            oikein = oikein + 1
            
        #tuloksen odotusarvo, sama kuin test-funktiossa
        E_a = 3/(1 + 10**((R_b - R_a)/400))
        E_b = 3/(1 + 10**((R_a - R_b)/400))
        
        home_name = game[0][0]
        away_name = game[1][0]

        joukkueet[home_name] = joukkueet[home_name] + E_a
        joukkueet[away_name] = joukkueet[away_name] + E_b    
        
            
        #muutetaan pelaajien ELO-lukuja todellisen tuloksen perusteella
        kaudet = [ [kausi[i]] ] #vastaa yhtä peliä ainoastaan
        p = train(p, kaudet, K, printOut = False)
        
    acc = oikein/len(kausi)
    return acc, joukkueet

kausi = kausi1617
acc, joukkueet = seuraava_peli(kausi, p)
print(acc)
