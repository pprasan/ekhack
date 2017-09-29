import pandas as pd
from datetime import datetime


def dayOfWeek(date):
    return str(date.weekday()+1)

def isWeekend(date):
    dayNum = date.weekday()
    if dayNum < 5:
        return "0"
    else:
        return "1"

def month(date):
    return str(date.month)

def printLine(lineList):
    line = ",".join(lineList)
    line += "\n"
    return line


pricingDF = pd.read_csv("../data/emirates/pricing.csv")

airport_dict = {}
with open("../data/external/airports.txt", "r") as airports:
    for line in airports:
        data = line.split(",")
        airport_dict[data[1].strip()] = data[0]
# To convert the airport code from three letter to ID,
# simply use, for instance = airport_dict['JFK']

with open("../data/emirates/parsedPricingData.csv", "w") as outputFile:
    for i, row in pricingDF.iterrows():
        line = []
        departureDate = datetime.strptime(row["DEPARTURE_DATE"], "%m/%d/%y")
        line.append(dayOfWeek(departureDate))
        line.append(isWeekend(departureDate))
        line.append(month(departureDate))

        #Write to file
        outputFile.write(printLine(line))

# why does DOW have many numbers?


# Assumptions:
# All fare in USD
