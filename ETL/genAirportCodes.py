import pandas as pd
import Utils

pricingDF = pd.read_csv("../data/emirates/pricing.csv")
with open("../data/external/airports.txt", "w") as outputFile:
    unsortedAirportCodes = set()
    for i, row in pricingDF.iterrows():
        if Utils.isBlank(row[Utils.ORIGIN]) or Utils.isBlank(row[Utils.DESTINATION]):
            continue
        unsortedAirportCodes.add(row[Utils.ORIGIN])
        unsortedAirportCodes.add(row[Utils.DESTINATION])

    airportCodes = sorted(unsortedAirportCodes)
    i = 1
    for code in airportCodes:
        outputFile.write(str(i) + "," + code + "\n")
        i += 1
    outputFile.close()
