import json
import numpy as np 

#convert spotify_id to a string
json_data = '{"spotify_id_1": {"name": "Pure Water", "artist": "Migos", "acousticness": 0.7, "volume": 0.2}, "spotify_id_2": {"name": "Cold Water", "artist": "Justin Bieber", "acousticness": 0.9, "volume": 1.6}}'

#with open("spotifysongs.json", "r") as f:
parsed_json = (json.loads(json_data))
#print(json.dumps(parsed_json, indent=4, sort_keys=True))

def generateArrays(json_data):
    loaded_json = json.loads(json_data)
    finalArray = []
    nameOfNums = []
    for key in loaded_json:
        #print("key:", key)
        ar = []
        ar.append(key)
        for smallkey in loaded_json[key]:
            #print("smallkey:", smallkey)
            value = loaded_json[key][smallkey]
            if type(value) is float:
                ar.append(value)
                nameOfNums.append(smallkey)
        #print("ar: ", ar)
        finalArray.append(ar)
    #print(finalArray)
    return finalArray, nameOfNums

def normalize(array):
    for x in range(len(array[0])):
        #ar = [max(subArray[x]) for subArray in array if type(subArray[x]) is float]
        ar = []
        for subArray in array:
            #print("subArray: ", subArray[x])
            if type(subArray[x]) is float:
                #print("subArray: ", subArray[x])
                ar.append(subArray[x])
        #print("ar: ", ar)
        if ar:
            largestVal = max(ar)
            for subArray in array:
                if type(subArray[x]) is float:
                    subArray[x] /= largestVal

generateArrays(json_data)

normalize(finalArray)
