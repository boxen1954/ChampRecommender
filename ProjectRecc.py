# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 16:04:10 2018

@author: Ethan Paulsen
"""

import requests

apiKey = "RGAPI-0c72f3b7-fccf-4a60-b112-114e69fa3044"

def getInfo():
    summonerName = input( "Please enter a summoner name, press Enter to exit: " )
 
    if summonerName is "":
        return ""
    
    print()

    summonerURL = 'https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + summonerName + '?api_key=' + apiKey
    #print( summonerURL )
    summonerInfo = requests.get( summonerURL ).json()
    summonerID = summonerInfo["accountId"]
    
    if "status" in summonerInfo:
        print( "Failure to get summoner ID." )
        print( *summonerInfo["status"].values(), sep = "  ")
        return ""
    print( "Summoner information retrieved!" )
    recentMatchLink = "https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/" + str( summonerID ) + "/recent?api_key=" + apiKey

    recentMatches = requests.get( recentMatchLink ).json()
    
    if "status" in recentMatches:
        print( "Error retrieving recent matches." )
        print( *recentMatches["status"].values(), sep = "  ")
        return ""
    print( "Recent match history retrieved!" )
    
    print("\n\n-----------------------------------------\n\n")
    for i in range( 0, len(recentMatches["matches"]) ):
        gameID = recentMatches["matches"][i]["gameId"]
        gameURL = "https://na1.api.riotgames.com/lol/match/v3/matches/" + str(gameID) + "?api_key=" + apiKey
        #print( gameURL )
        #print()
        gameJSON = requests.get( gameURL ).json()
        
        if "status" in gameJSON:
            print( "Failure to retrieve game statistics." )
            print( *gameJSON["status"].values(), sep = "  ")
            return ""
        print( "Game information retrieved!" )
        print()
        participant = {}
        for item in gameJSON["participantIdentities"]:
            if item["player"].get("summonerName") == summonerName:
                index = item["participantId"]
                participant = gameJSON["participants"][index - 1]
                
        champURL = "https://na1.api.riotgames.com/lol/static-data/v3/champions/" + str( recentMatches["matches"][i]["champion"] ) + "?locale=en_US&champData=tags&api_key=" + apiKey
        champNameJSON = requests.get( champURL ).json()
        if "status" in champNameJSON:
            print( "Failure to retrieve champion statistics." )
            print( "Error:", *champNameJSON["status"].values(), sep = "  ")
            return ""
        print( "Champion information retrieved!" )
        print()
        print( "This summoner played " + str( champNameJSON["name"] ) + " in their last game."  )
        print( "Their KDA was ", str(participant["stats"]["kills"]).strip(), "/", str(participant["stats"]["deaths"]).strip(), "/", str(participant["stats"]["assists"]).strip() )
        print()
    return summonerName

getInfo()