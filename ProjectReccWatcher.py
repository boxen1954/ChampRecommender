# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 19:22:27 2018

@author: Ethan Paulsen
"""

#This is a test using the riotwatcher library.
from urllib.request import urlopen
from bs4 import BeautifulSoup
from riotwatcher import RiotWatcher as rw
from pathlib import Path
import requests
import csv
import numpy as np
import matplotlib.pyplot as plt

def grabOtherPlayers():
    api_key="RGAPI-0c72f3b7-fccf-4a60-b112-114e69fa3044"
    watcher = rw(api_key)
    dicti = {}
    otherPlayerList = []
    response = urlopen("https://www.leagueofgraphs.com/rankings/summoners/na")
    soup = BeautifulSoup(response, "lxml")
    static_data = open('static_champ_list.csv','r')
    crossReference = {}
    firstRow = True
    for row in static_data:
        token = row.split(',')
        if firstRow == True:
            firstRow = False
            pass
        else:
            Id = token[0]
            name = token[1]
            crossReference[int(Id)] = name
    static_data.close()
    print(crossReference)
    count = 0
    for child in soup.find_all("span", { "class" : "name"}):
        if count != 3:
            count = count + 1
            player = child.get_text()
            dicti[player] = {}
            originalChamps = []
            player = player.lstrip()
            otherPlayerList.append(player)
            me = watcher._summoner.by_name( "na1", player )
            accountId = me['accountId']
            print("Summoner found.\n\n" )
            print( me )
            print(accountId)
            print("\n\n------------------------------------------\n\n" )
            recentMatches = watcher._match.matchlist_by_account("na1", accountId, begin_index=0, end_index=20)
            print("recent: " , recentMatches)
            for i in range(len(recentMatches['matches'])):
                gameId = recentMatches['matches'][i]['gameId']
                champId = recentMatches['matches'][i]['champion']
                if champId not in originalChamps:
                    originalChamps.append(champId)
                    print('gameId: ' + str(recentMatches['matches'][i]['gameId']))
                    print('champId: ' + str(recentMatches['matches'][i]['champion']))
                    gameStats = watcher.match.by_id('na1',gameId)
                    for i in range(len(gameStats['participants'])):
                        if gameStats['participants'][i]['championId'] == champId:
                            stat_kills = gameStats['participants'][i]['stats']['kills']
                            print('kills: ' + str(stat_kills))
                            stat_deaths = gameStats['participants'][i]['stats']['deaths']
                            print('deaths: ' + str(stat_deaths))
                            try:
                                KDrat = stat_kills/stat_deaths
                            except:
                                KDrat = stat_kills
                            print(KDrat)
                            dicti[player][crossReference[champId]] = KDrat
                        else:
                            pass
                else:
                    pass
        else:
            print(dicti) 
            break
          
               
def checkFile( my_region ):
    api_key="RGAPI-0c72f3b7-fccf-4a60-b112-114e69fa3044"
    watcher = rw(api_key)
    print( "Watcher Established." )
    print()
    print( "-------------------------------------------------" )
    p = Path(".")
    myfile = p / "static_champ_list.csv"
    champURL = "https://na1.api.riotgames.com/lol/static-data/v3/champions?locale=en_US&champData=stats&tags=tags&tags=info&api_key=" + api_key
    static = watcher._static_data
    champNameJSON = static.champions(my_region, tags=['tags','info'])
    #if "status" in champNameJSON:
    #   print( "Failure to retrieve champion statistics." )
    #  print( "Error:", *champNameJSON["status"].values(), sep = "  ")
    #fp = open( "static_champ_list.csv", "w" )
    with open("static_champ_list.csv" , "w") as fp:
        fp.write('id,name,primary,secondary,attack,defense,magic,difficulty' + '\n')
        #print( champNameJSON["data"] )
        for champ in champNameJSON["data"].values():
            #print('champ: ' , champ)
            #fp.write( str(champ["id"]) , "," )
            #fp.write(champ["name"] , "," );
            fp.write(str(champ['id']) + ',')
            fp.write(champ['name'] + ',')
            if len(champ["tags"]) > 1:
                for typ in champ["tags"]:
                    fp.write( typ + ",")
            else:
                fp.write( champ["tags"][0] + ",null," )
            count = 0;
            for item in champ["info"].values():
                if( count != 3 ):
                    fp.write( str(item) + "," )
                    count = count + 1
                else:
                    fp.write( str(item) + "\n" )
        fp.close()
        return 0
    print( "Static champion list found." )
    print( "\n\n---------------------------------------\n\n" )

def getInfo():
    watcher = rw("RGAPI-0c72f3b7-fccf-4a60-b112-114e69fa3044")
    regionList = ["na1", "euw1", "eun1", "kr", "ru", "jp1", "oc1", "tr1", "la1", "la2" ]
    my_region = input( "Enter your region, press enter to quit. For a list of regions, please type region: " )
    print()
    while my_region == "region":
        print( "The different regions are:" )
        print( *regionList, sep="\n" )
        my_region = input( "Enter your region, press enter to quit. For a list of regions, please type region: " )
    summonerName = input( "Please enter a name, hit Enter to quit: " )
    print()

    if summonerName == "":
        return ""

    checkFile( my_region )
    me = watcher._summoner.by_name( my_region, summonerName )
    accountId = me['accountId']
    print("Summoner found.\n\n" )
    print( me )
    print(accountId)
    print("\n\n------------------------------------------\n\n" )
    recentMatches = watcher._match.matchlist_by_account(my_region, accountId, begin_index=0, end_index=20)
    print("recent: " , recentMatches)
#    gameId = []
#    champPicked = []
#    infoRetrieved = {}
#    for game in recentMatches["matches"]:
#        gameId.append( game["gameId"] )
#        champPicked.append( game["champion"] )
#    
#    fp = open( "static_champ_list.csv", "r" )
#    for line in fp:
#        print( line )
#    for x in range( 0, 20 ):
#    gamePlayed = watcher.match.by_id( my_region, gameId[0] );
#   print( gamePlayed )
#    for line in fp:
#        if champPicked[0] in line:
#            gameData = {}
#            string = fp.readline( line ).split(",");
#            gameData.update( { "champion" : string[1] } )
#            if "0" in line:
#                gameData.update( { "tag": string[2] } )
#                gameData.update( { "info" : [ string[4], string[5], string[6], string[7] ] } )
#            else:
#                gameData.update( {"tags", [string[3], string[4]] })
#                gameData.update( { "info" : [ string[5], string[6], string[7], string[8] ] } )
#            print( gameData )
#            print()
#            print()
#            infoRetrieved.update( { 0 : gameData } )
                
#    fp.close()
    userStats = open('user_Stats.csv', 'w')
    userStats.write('champId,kills,deaths,assists,KD ratio' + '\n')
    for i in range(len(recentMatches['matches'])):
        gameId = recentMatches['matches'][i]['gameId']
        champId = recentMatches['matches'][i]['champion']
        print('gameId: ' + str(recentMatches['matches'][i]['gameId']))
        print('champId: ' + str(recentMatches['matches'][i]['champion']))
        gameStats = watcher.match.by_id('na1',gameId)
        for i in range(len(gameStats['participants'])):
            if gameStats['participants'][i]['championId'] == champId:
                stat_kills = gameStats['participants'][i]['stats']['kills']
                print('kills: ' + str(stat_kills))
                stat_deaths = gameStats['participants'][i]['stats']['deaths']
                print('deaths: ' + str(stat_deaths))
                stat_assists = gameStats['participants'][i]['stats']['assists']
                print('assists: ' + str(stat_assists))
                KDratio =  stat_kills/stat_deaths
                print('KDRatio: ' + str(KDratio))
                userStats.write(str(champId) + ',' + str(stat_kills) + ',' + str(stat_deaths) + ',' + str(stat_assists) + ',' + str(KDratio) + '\n')
    userStats.close()
    
def recommend(userInfo, staticInfo):
    import operator
    staticStats = open(staticInfo, 'r')
    token = csv.reader(staticStats, delimiter=',')
    champIDToPrimary = {}
    numOfPrimary = {}
    firstRow = True
    champAlreadyPlayed = []
    recommendations = []
    maxVal = 0
    maxVal = float(maxVal)
    maxChampId = 0
    for row in token:
        if firstRow == True:
            firstRow = False
            pass
        else:
            championId = row[0]
            primaryStat = row[2]
            champIDToPrimary[championId] = primaryStat
    staticStats.close()
    #print("champIDToPrimary: " , champIDToPrimary)
    userStats = open(userInfo, 'r')
    token1 = csv.reader(userStats, delimiter=',')
    firstRow = True
    for row1 in token1:
        if firstRow == True:
            firstRow = False
            pass
        else:
            champId = row1[0]
            KDrat = float(row1[4])
            print("max: " + str(maxVal))
            print("Kd: " + str(KDrat))
            if KDrat > maxVal:
                maxVal = KDrat
                maxChampId = champId
            print(maxChampId + "," + maxVal)
    userStats.close()
    #print(numOfPrimary)
    #print(highestCategory)
    for c in champIDToPrimary:
        value = champIDToPrimary[c]
        if value == highestCategory:
            if c not in champAlreadyPlayed:
                recommendations.append(c)
            else:
                pass
def visualize():
    stat = open('static_champ_list.csv' , 'r')
    masterList = []
    attackList = []
    defenseList = []
    magicList = []
    difficultyList = []
    nameList = []
    titles = ['Attacks','Defense','Magic','Difficulty']
    firstRow = True
    for row in stat:
        token = row.split(',')
        if firstRow == True:
            firstRow = False
            pass
        else:
            attack = token[4]
            attackList.append(attack)
            defense = token[5]
            defenseList.append(defense)
            magic = token[6]
            magicList.append(magic)
            difficulty = token[7]
            difficultyList.append(difficulty.strip())
            name = token[1]
            nameList.append(name)
    masterList.append(attackList)
    masterList.append(defenseList)
    masterList.append(magicList)
    masterList.append(difficultyList)
    print(masterList)
    fig = plt.figure()
    plotno = 221
    for x in range(len(masterList)):
        print(plotno)
        li = masterList[x]
        print("li: " , li)
        ax = fig.add_subplot(plotno)
        N = len(attackList)
        ind = np.arange(N)
        width = 0.20
        rect = ax.bar(ind, li, width, color='red')
        xtickNames = ax.set_xticklabels(nameList)
        ax.set_xlabel('Names')
        ax.set_title(titles[x])
        plt.setp(xtickNames, fontsize=10, rotation=90)
        plotno += 1
    plt.show()
grabOtherPlayers()        
#getInfo()
#recommend('user_Stats.csv' , 'static_champ_list.csv')
#visualize()
    