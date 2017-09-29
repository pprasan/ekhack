import pandas as pd

ORIGIN = "ORIG"
DESTINATION = "DEST"

def isBlank(string):
    s = str(string)
    return not bool(s and s.strip())


pricingDF = pd.read_csv("../data/emirates/pricing.csv")
with open("../data/external/airports.txt", "w") as outputFile:
    unsortedAirportCodes = set()
    for i, row in pricingDF.iterrows():
        if isBlank(row[ORIGIN]) or isBlank(DESTINATION):
            continue
        unsortedAirportCodes.add(row[ORIGIN])
        unsortedAirportCodes.add(row[DESTINATION])

    airportCodes = sorted(unsortedAirportCodes)
    i = 1
    for code in airportCodes:
        outputFile.write(str(i) + "," + code + "\n")
        i += 1
    outputFile.close()
