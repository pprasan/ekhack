import pandas as pd
from datetime import datetime


def dayOfWeek(date):
    return str(date.weekday() + 1)


def isWeekend(date):
    dayNum = date.weekday()
    if dayNum < 5:
        return "0"
    else:
        return "1"


def month(date):
    return str(date.month)


def travelSpan():
    return "1"  # FIXME


def marketShare(ms_perc):
    return str(ms_perc / 100.0)


def printLine(lineList):
    line = ",".join(lineList)
    line += "\n"
    return line


pricingDF = pd.read_csv("../data/emirates/pricing.csv")


def loadOilPrices():
    oil_dict = {}
    with open("../data/external/oilPricesChange.csv", "r") as prices:
        for line in prices:
            data = line.split(",")
            dateOrigFormat = data[0]
            date = datetime.strptime(dateOrigFormat.strip(), "%Y-%m-%d")
            oil_dict[date] = data[2].strip()
    return oil_dict

def loadAirportData():
    airport_dict = {}
    with open("../data/external/airports.txt", "r") as airports:
        for line in airports:
            data = line.split(",")
            airport_dict[data[1].strip()] = data[0]
    return airport_dict
    # To convert the airport code from three letter to ID,
    # simply use, for instance = airport_dict['JFK']


airport_dict = loadAirportData()
oil_dict = loadOilPrices()

def airportID(airportCode):
    return airport_dict[airportCode]


with open("../data/emirates/parsedPricingData.csv", "w") as outputFile:
    headerLine = ["fareID",
                  "dayOfWeek",
                  "isWeekend",
                  "month",
                  "travelSpan",
                  "marketShare",
                  # "orig",
                  # "dest,
                  "fuelAndInsurance",
                  "fuelSurcharge",
                  "baseFare",
                  "taxes",
                  "miscAmt",
                  "totalAmt",
                  "changeInOilPrice"
                  ]
    outputFile.write(printLine(headerLine))
    for i, row in pricingDF.iterrows():
        line = []

        #Input Values
        line.append(str(row["FAREID"]))
        departureDate = datetime.strptime(row["DEPARTURE_DATE"], "%m/%d/%y")
        line.append(dayOfWeek(departureDate))
        line.append(isWeekend(departureDate))
        line.append(month(departureDate))
        line.append(travelSpan())
        line.append(marketShare(row["MS_PERC"]))
        # line.append(airportID(row["ORIG"])) #origin
        # line.append(airportID(row["DEST"])) #destination

        #Output Values
        line.append(str(row["YQ_YR_AMT_BC"])) #Fuel & Insurance
        line.append(str(row["Q_FUEL_AMT_BC"])) #Fuel Surcharge
        line.append(str(row["FAREAMT_BC"])) #Base Fare
        line.append(str(row["TAX_AMT_BC"])) #TAX TAX TAX
        line.append(str(row["Q_OTHERS_AMT_BC"])) #Other Shit
        line.append(str(row["TOTAL_AMT_BC"])) #Total Amount

        # Write to file
        outputFile.write(printLine(line))

# why does DOW have many numbers?


# Assumptions:
# All fare in USD
