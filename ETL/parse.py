import pandas as pd
from datetime import datetime, timedelta

# FIELD COLUMN LABELS
FARE_ID = "FAREID"
DEPARTURE_DATE = "DEPARTURE_DATE"
MARKET_SHARE = "MS_PERC"
ORIGIN = "ORIG"
DESTINATION = "DEST"
FARE_FUEL_INSURANCE = "YQ_YR_AMT_BC"
FARE_FUEL_SURCHARGE = "Q_FUEL_AMT_BC"
FARE_BASE = "FAREAMT_BC"
FARE_TAX = "TAX_AMT_BC"
FARE_MISC = "Q_OTHERS_AMT_BC"
FARE_TOTAL = "TOTAL_AMT_BC"


def isBlank(string):
    s = str(string)
    return not bool(s and s.strip())


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


def findClosetOilPrice(date):
    dateTime = datetime.strptime(date, "%m/%d/%y")
    count = 0
    while dateTime not in oil_dict:
        if count > 10:
            return ''  # disregard if older than 10 days
        dateTime -= timedelta(days=1)
        count += 1
    return oil_dict[dateTime]


pricingDF = pd.read_csv("../data/emirates/pricing.csv")
with open("../data/emirates/parsedPricingData.csv", "w") as outputFile:
    headerLine = ["fareID",
                  "dayOfWeek",
                  "isWeekend",
                  "month",
                  "travelSpan",
                  "marketShare",
                  "origin",
                  "destination",
                  # "changeInOilPrice",
                  "fuelAndInsurance",
                  "fuelSurcharge",
                  "baseFare",
                  "taxes",
                  "miscAmt",
                  "totalAmt"
                  ]
    outputFile.write(printLine(headerLine))
    for i, row in pricingDF.iterrows():
        if (row is None) or \
                isBlank(row[FARE_ID]) or \
                isBlank(row[DEPARTURE_DATE]) or \
                isBlank(row[MARKET_SHARE]) or \
                isBlank(row[ORIGIN]) or \
                isBlank(row[DESTINATION]) or \
                isBlank(row[FARE_FUEL_INSURANCE]) or \
                isBlank(row[FARE_FUEL_SURCHARGE]) or \
                isBlank(row[FARE_BASE]) or \
                isBlank(row[FARE_TAX]) or \
                isBlank(row[FARE_MISC]) or \
                isBlank(row[FARE_TOTAL]):
            continue

        # Input Values
        line = [str(row[FARE_ID])]
        departureDate = datetime.strptime(row[DEPARTURE_DATE], "%m/%d/%y")
        line.append(dayOfWeek(departureDate))
        line.append(isWeekend(departureDate))
        line.append(month(departureDate))
        line.append(travelSpan())
        line.append(marketShare(row[MARKET_SHARE]))
        line.append(airportID(row[ORIGIN]))  # origin
        line.append(airportID(row[DESTINATION]))  # destination
        oilPrice = findClosetOilPrice(row[DEPARTURE_DATE])  # probably need to give purchase date?
        # line.append(oilPrice)

        # Output Values
        line.append(str(row[FARE_FUEL_INSURANCE]))  # Fuel & Insurance
        line.append(str(row[FARE_FUEL_SURCHARGE]))  # Fuel Surcharge
        line.append(str(row[FARE_BASE]))  # Base Fare
        line.append(str(row[FARE_TAX]))  # TAX TAX TAX
        line.append(str(row[FARE_MISC]))  # Other Shit
        line.append(str(row[FARE_TOTAL]))  # Total Amount

        # Write to file
        outputFile.write(printLine(line))

# why does DOW have many numbers?


# Assumptions:
# All fare in USD
