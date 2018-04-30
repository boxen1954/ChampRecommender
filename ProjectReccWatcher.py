# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 19:22:27 2018

@author: Ethan Paulsen
"""

#This is a test using the riotwatcher library.

from riotwatcher import RiotWatcher as rw
from pathlib import Path
import requests

def checkFile( my_region ):
    api_key="RGAPI-0c72f3b7-fccf-4a60-b112-114e69fa3044"
    watcher = rw(api_key)
    print( "Watcher Established." )
    print()
    print( "-------------------------------------------------" )
    p = Path(".")
    myfile = p / "static_champ_list.csv"
    champURL = "https://na1.api.riotgames.com/lol/static-data/v3/champions?locale=en_US&champData=stats&tags=tags&tags=info&api_key=" + api_key
    champNameJSON = watcher.static_data.champions( "stats", "tags" ).json()
    #if "status" in champNameJSON:
    #   print( "Failure to retrieve champion statistics." )
    #  print( "Error:", *champNameJSON["status"].values(), sep = "  ")
    #fp = open( "static_champ_list.csv", "w" )
    with open("static_champ_list.csv" , "w") as fp:
        fp.write('id,name,primary,secondary,attack,defense,magic,difficulty' + '\n')
        print( champNameJSON["data"] )
        for champ in champNameJSON["data"].values():
            print('champ: ' , champ)
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
        print( "Error creating object" )
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

    me = watcher.summoner.by_name( my_region, summonerName )
    
    print("Summoner found.\n\n" )
    print( me )
    print("\n\n------------------------------------------\n\n" )
    recentMatches = watcher.match.matchlist_by_account_recent( my_region, me["accountId"] )
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
    for i in range(len(recentMatches['matches'])):
        gameId = recentMatches['matches'][i]['gameId']
        champId = recentMatches['matches'][i]['champion']
        print('gameId: ' + str(recentMatches['matches'][i]['gameId']))
        print('champId: ' + str(recentMatches['matches'][i]['champion']))
        gameStats = watcher.match.matches(gameId)
        print('gameStats: ' , gameStats)
getInfo()