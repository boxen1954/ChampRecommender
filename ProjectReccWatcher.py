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
from math import sqrt
import math

def grabOtherPlayers(my_region):
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
    #print(crossReference)
    count = 0
    for child in soup.find_all("span", { "class" : "name"}):
        #Number of players wanted
        if count != 10:
            count = count + 1
            player = child.get_text()
            dicti[player] = {}
            originalChamps = []
            player = player.lstrip()
            otherPlayerList.append(player)
            me = watcher._summoner.by_name( "na1", player )
            accountId = me['accountId']
            print("\n\nStatic Summoner found: ", player, ".\n\n" )
            #print( me )
            #print(accountId)
            #print("\n\n------------------------------------------\n\n" )
            recentMatches = watcher._match.matchlist_by_account("na1", accountId, begin_index=0, end_index=20)
            #print("recent: " , recentMatches)
            for i in range(len(recentMatches['matches'])):
                gameId = recentMatches['matches'][i]['gameId']
                champId = recentMatches['matches'][i]['champion']
                if champId not in originalChamps:
                    originalChamps.append(champId)
                    #print('gameId: ' + str(recentMatches['matches'][i]['gameId']))
                    #print('champId: ' + str(recentMatches['matches'][i]['champion']))
                    gameStats = watcher.match.by_id('na1',gameId)
                    for i in range(len(gameStats['participants'])):
                        if gameStats['participants'][i]['championId'] == champId:
                            stat_kills = gameStats['participants'][i]['stats']['kills']
                            #print('kills: ' + str(stat_kills))
                            stat_deaths = gameStats['participants'][i]['stats']['deaths']
                            #print('deaths: ' + str(stat_deaths))
                            try:
                                KDrat = stat_kills/stat_deaths
                            except:
                                KDrat = stat_kills
                            #print(KDrat)
                            dicti[player][crossReference[champId]] = KDrat
                        else:
                            pass
                else:
                    pass
        else:
            #print(dicti) 
            return dicti
          
def checkFile( my_region ):
    api_key="RGAPI-0c72f3b7-fccf-4a60-b112-114e69fa3044"
    watcher = rw(api_key)
    print( "Watcher Established." )
    print()
    print( "-------------------------------------------------" )
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

def recommender(summonerName, dicti):
    ds = computeNearestNeighbor(0, summonerName,dicti)
    print("Nearest Neighbor: " , ds)
    print()
    rec = recommend(0, summonerName, dicti)
    print("Recommendations based on nearest neighbor:")
    for r in rec:
        print(r[0] , " ---> " , r[1])
    visualize( rec )
#    import operator
#    staticStats = open(staticInfo, 'r')
#    token = csv.reader(staticStats, delimiter=',')
#    champIDToPrimary = {}
#    numOfPrimary = {}
#    firstRow = True
#    champAlreadyPlayed = []
#    recommendations = []
#    maxVal = 0
#    maxVal = float(maxVal)
#    maxChampId = 0
#    for row in token:
#        if firstRow == True:
#            firstRow = False
#            pass
#        else:
#            championId = row[0]
#            primaryStat = row[2]
#            champIDToPrimary[championId] = primaryStat
#    staticStats.close()
#    #print("champIDToPrimary: " , champIDToPrimary)
#    userStats = open(userInfo, 'r')
#    token1 = csv.reader(userStats, delimiter=',')
#    firstRow = True
#    for row1 in token1:
#        if firstRow == True:
#            firstRow = False
#            pass
#        else:
#            champId = row1[0]
#            KDrat = float(row1[4])
#            print("max: " + str(maxVal))
#            print("Kd: " + str(KDrat))
#            if KDrat > maxVal:
#                maxVal = KDrat
#                maxChampId = champId
#            print(maxChampId + "," + maxVal)
#    userStats.close()
#    #print(numOfPrimary)
#    #print(highestCategory)
#    for c in champIDToPrimary:
#        value = champIDToPrimary[c]
#        if value == highestCategory:
#            if c not in champAlreadyPlayed:
#                recommendations.append(c)
#            else:
#                pass

def getInfo():
    watcher = rw("RGAPI-0c72f3b7-fccf-4a60-b112-114e69fa3044")
    regionList = ["na1", "euw1", "eun1", "kr", "ru", "jp1", "oc1", "tr1", "la1", "la2" ]
    my_region = input( "Enter your region, press enter to quit. For a list of regions, please type region: " )
    print()
    while (my_region == "region") or (my_region not in regionList):
        print( "The different regions are:" )
        print( *regionList, sep="\n" )
        my_region = input( "Enter your region, press enter to quit. For a list of regions, please type region: " )
    summonerName = input( "Please enter a name, hit Enter to quit: " )
    print()

    if summonerName == "":
        return ""

    checkFile( my_region )
    dicti = grabOtherPlayers(my_region)
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
    me = watcher._summoner.by_name( my_region, summonerName )
    accountId = me['accountId']
    print("Summoner found", summonerName, ".\n\n" )
    print("\n\n------------------------------------------\n\n" )
    recentMatches = watcher._match.matchlist_by_account(my_region, accountId, begin_index=0, end_index=20)

    dicti[summonerName] = {}
    champList = {}
    for i in range(len(recentMatches['matches'])):
        gameId = recentMatches['matches'][i]['gameId']
        champId = recentMatches['matches'][i]['champion']
        #print('gameId: ' + str(recentMatches['matches'][i]['gameId']))
        #print('champId: ' + str(recentMatches['matches'][i]['champion']))
        if champId not in champList:
            champList[crossReference[champId]] = []
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
                print( "KDRatio: ", KDrat )
                print( "\n" )
                dicti[summonerName][crossReference[champId]] = KDrat
                if crossReference[champId] in champList:
                    champList[crossReference[champId]].append( KDrat )
    #print(dicti)
    for item in champList.values():
        try:
            newData = sum(item)/len(item)
            item.clear()
            item.append(newData)
        except ZeroDivisionError as e:
            print( e.with_traceback )
            pass
    recommender(summonerName, dicti)
    
def manhattan(rating1, rating2):
    """Computes the Manhattan distance. Both rating1 and rating2 are dictionaries
    """
    distance = 0
    commonRatings = False 
    for key in rating1:
        if key in rating2:
            distance += abs(rating1[key] - rating2[key])
            commonRatings = True
    if commonRatings:
        return distance
    else:
        return -1 #Indicates no ratings in common

def computeNearestNeighbor(r, username, users):
    """creates a sorted list of users based on their distance to username"""
    distances = []
    for user in users:
        if user != username:
            if ( r == 1 ) or ( r == 2 ):
                distance = minkowski(r, users[user], users[username])
                distances.append((round(distance, 2), user))
            if (r == 0 ):
                distance = pearson(users[user], users[username])
                distances.append((round(distance, 2), user))
    # sort based on distance -- closest first
    if ( r == 1 ) or ( r == 2 ):
        distances.sort()
    if( r == 0 ):
        distances.sort(reverse=True)
    return distances


def recommend(r ,username, users):
    """Give list of recommendations"""
    # first find nearest neighbor
    nearest = computeNearestNeighbor(r, username, users)[0][1]
    recommendations = []
    # now find bands neighbor rated that user didn't
    neighborRatings = users[nearest]
    userRatings = users[username]
    for artist in neighborRatings:
        if not artist in userRatings:
            recommendations.append((artist, neighborRatings[artist]))
    # using the fn sorted for variety - sort is more efficient
    return sorted(recommendations, key=lambda artistTuple: artistTuple[1], reverse = True)

def minkowski(r, rating1, rating2):
    """Computes the Euclidean distance. Both rating1 and rating2 are dictionaries"""
    distance = 0
    commonRatings = False 
    for key in rating1:
        if key in rating2:
            distance += math.pow((abs(rating1[key] - rating2[key])), r)
            commonRatings = True
    if commonRatings:
        distance = math.pow(distance, 1/r)
        return distance
    else:
        return -1 #Indicates no ratings in common

def pearson(rating1, rating2):
    sum_xy = 0
    sum_x = 0
    sum_y = 0
    sum_x2 = 0
    sum_y2 = 0
    n = 0
    for key in rating1:
        if key in rating2:
            n += 1
            x = rating1[key]
            y = rating2[key]
            sum_xy += x * y
            sum_x += x
            sum_y += y
            sum_x2 += pow(x, 2)
            sum_y2 += pow(y, 2)
    if n == 0:
        return 0
    # now compute denominator
    denominator = (sqrt(sum_x2 - pow(sum_x, 2) / n)
                   * sqrt(sum_y2 - pow(sum_y, 2) / n))
    if denominator == 0:
        return 0
    else:
        return (sum_xy - (sum_x * sum_y) / n) / denominator    
    

def visualize( champReccList ):
    stat = open('static_champ_list.csv' , 'r')
    masterList = []
    attackList = []
    defenseList = []
    magicList = []
    difficultyList = []
    nameList = []
    titles = ['Attacks','Defense','Magic','Difficulty']
    firstRow = True
    count = 0;
    for row in stat:
      #  print( champReccList[count][0] )
        token = row.split(',')
        print( token )
        if firstRow == True:
            firstRow = False
        else:
            for count in range (0, len(champReccList) ):
                if champReccList[count][0] in token:
                    print( "Token found." )
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
    #print(masterList)
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

    
getInfo()
#visualize()

    
