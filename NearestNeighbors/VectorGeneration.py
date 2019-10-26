import json
import numpy as np 

#convert spotify_id to a string
json_data = '{"spotify_id_1": {"name": "Pure Water", "artist": "Migos", "acousticness": 0.7}, "spotify_id_2": {"name": "Cold Water", "artist": "Justin Bieber", "acousticness": 0.9}}'

def generateArrays(json_data):
    loaded_json = json.loads(json_data)
    finalArray = []
    for key in loaded_json:
        #print("key:", key)
        ar = []
        ar.append(key)
        for smallkey in loaded_json[key]:
            #print("smallkey:", smallkey)
            ar.append(loaded_json[key][smallkey])
        #print("ar: ", ar)
        finalArray.append(ar)
    #print(finalArray)
    return finalArray

 generateArrays(json_data)