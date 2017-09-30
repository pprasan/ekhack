import os
import pandas as pd
import urllib
import urllib2
import json

dict = {}
with open("../data/external/city-airport.csv", "r") as outputFile:
    for line in outputFile:
        # print line.strip()
        data = line.split(',')
        arr = []
        if len(data) == 1:
            data.append(data[0])
        for a in data:
            arr.append(a.strip())
        dict[data[0].strip()] = data[1].strip()

def getDistance(origin, dest):
    url = 'http://www.distance24.org/route.json'
    param = origin+"|"+dest
    values = {'stops' : param}

    data = urllib.urlencode(values)
    response = urllib2.urlopen(url+ '?' + data)
    return json.load(response)["distance"]


pricingDF = pd.read_csv("../data/emirates/pricing.csv")
with open("../data/emirates/city-distance.csv", "w") as outputFile:
    distanceDict = {}
    for i, row in pricingDF.iterrows():
        try:
            key = row["ORIG"] + ':' + row["DEST"]
            if key in distanceDict:
                continue
            else:                
                distance = getDistance(dict[row["ORIG"]], dict[row["DEST"]])
                print row["ORIG"] + ':' + row["DEST"] +  ',' + str(distance)
                distanceDict[row["ORIG"] + ':' + row["DEST"]] = str(distance)
            # print row["ORIG"] + ' ' + row["DEST"] + ' ----> ' + dict[row["ORIG"]] + ' ' + dict[row["DEST"]] + ' --> ' + str(distance)
        except ValueError as e:
            # print 'FAILED FOR ' + row["ORIG"] + ' ' + row["DEST"] + ' ----> ' + dict[row["ORIG"]] + ' ' + dict[row["DEST"]]
            # print e
            continue

    for keyvalue in distanceDict.items():
        key, value = keyvalue[0], keyvalue[1]
        outputFile.write(key+','+value+'\n')
