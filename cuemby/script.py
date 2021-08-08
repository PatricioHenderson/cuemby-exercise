#!/usr/bin/env python

__author__ = "Patricio Henderson"
__email__ = "patricio.henderson.v@gmail.com"
__version__ = "1.0"

import json
from requests.models import CaseInsensitiveDict

import tinymongo as tm
import tinydb
import requests
import aiohttp
import asyncio
asyncio.set_event_loop(asyncio.new_event_loop())



# Bug: https://github.com/schapman1974/tinymongo/issues/58
class TinyMongoClient(tm.TinyMongoClient):
    @property
    def _storage(self):
        return tinydb.storages.JSONStorage

db_name = 'players'   

def clear():
    conn = TinyMongoClient()
    db = conn[db_name]
    
    
    # Delete al existing documents of players colection
    
    db.players.remove({})

    # Close db conection
    conn.close()




async def fetch():


    url = 'https://www.easports.com/fifa/ultimate-team/api/fut/item?page=1'
    
    response = requests.get(url)
    dataset = response.json()
    totalpages = dataset['totalPages']
    filtrado = []
    
    # First getting how many pages are, to be able to look for the information in all of them.
    # coroutines are used to make faster the web scraping
    for i in range(1,totalpages):
        try:
            asyncio.set_event_loop(asyncio.new_event_loop())
            loop = asyncio.new_event_loop() 
            asyncio.get_event_loop()
            url = 'https://www.easports.com/fifa/ultimate-team/api/fut/item?page={}' .format(i)
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    
                    dataset = await response.json()
                    json_response = dataset["items"]
    
                    filtrado += [{"name": x['name'] ,'lastName':  x["lastName"], "position": x["position"] ,"nationality" : x["nation"]["abbrName"] , "team" : x["club"]["abbrName"] } for x in json_response]

                    await asyncio.gather(insert_player(filtrado))
        except:
            pass

    return  filtrado



async def insert_player(dataset):
    conn = TinyMongoClient()
    db = conn[db_name]
 
    for i in dataset:
        player_json ={"name" : i["name"] ,'lastName' : i['lastName'] ,"position": i["position"], "nationality": i["nationality"] , "team": i["team"] }
        try:
            
            if db.players.find({"name" : i["name"] , 'lastName' : i['lastName'] }).count() != 0:
                pass
            else:
                db.players.insert_one(player_json) 
            
            
        except:
            pass


    
    conn.close()

def find_team(name):
    conn = TinyMongoClient()
    db = conn[db_name]
    
    name = name.title() 
    cursor = db.players.find({'team'  : name})
    data = list(cursor)
    json_string = json.dumps(data,indent=4)
    print(json_string)
    conn.close()
    return json_string

def find_player(name,order):
    conn = TinyMongoClient()
    db = conn[db_name]


    name = name.title() 
    cursor = db.players.find({'$or': {'name'  : name ,'lastName' : name }}).sort({'name' : order})
    data = list(cursor)
    json_string = json.dumps(data,indent=4)
    print(json_string)
    conn.close()
    return json_string





if __name__ == "__main__":
    
    clear()
    asyncio.run(fetch())
    dataset = fetch()
    insert_player(dataset)
    find_team("juventus")
    find_player('messi',-1)
    


