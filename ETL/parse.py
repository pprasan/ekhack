import pandas as pd
import Utils
from datetime import datetime, timedelta


def dayOfWeek(date):
    return str(date.weekday() + 1)


def isWeekend(date):
    if date.weekday() < 5:
        return "0"
    else:
        return "1"


def month(date):
    return str(date.month)


def travelSpan():
    return "1"  # FIXME


def marketShare(value):
    return str(value / 100.0)


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
    airports = pd.read_csv("../data/external/airports.csv")
    for i, line in airports.iterrows():
        airport_dict[line['AirportCode']] = str(line['Num'])
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
                Utils.isBlank(row[Utils.FARE_ID]) or \
                Utils.isBlank(row[Utils.DEPARTURE_DATE]) or \
                Utils.isBlank(row[Utils.MARKET_SHARE]) or \
                Utils.isBlank(row[Utils.ORIGIN]) or \
                Utils.isBlank(row[Utils.DESTINATION]) or \
                Utils.isBlank(row[Utils.FARE_FUEL_INSURANCE]) or \
                Utils.isBlank(row[Utils.FARE_FUEL_SURCHARGE]) or \
                Utils.isBlank(row[Utils.FARE_BASE]) or \
                Utils.isBlank(row[Utils.FARE_TAX]) or \
                Utils.isBlank(row[Utils.FARE_MISC]) or \
                Utils.isBlank(row[Utils.FARE_TOTAL]):
            continue

        # Input Values
        line = [str(row[Utils.FARE_ID])]
        departureDate = datetime.strptime(row[Utils.DEPARTURE_DATE], "%m/%d/%y")
        line.append(dayOfWeek(departureDate))
        line.append(isWeekend(departureDate))
        line.append(month(departureDate))
        line.append(travelSpan())
        line.append(marketShare(row[Utils.MARKET_SHARE]))
        line.append(airportID(row[Utils.ORIGIN]))  # origin
        line.append(airportID(row[Utils.DESTINATION]))  # destination
        oilPrice = findClosetOilPrice(row[Utils.DEPARTURE_DATE])  # probably need to give purchase date?
        # line.append(oilPrice)

        # Output Values
        line.append(str(row[Utils.FARE_FUEL_INSURANCE]))  # Fuel & Insurance
        line.append(str(row[Utils.FARE_FUEL_SURCHARGE]))  # Fuel Surcharge
        line.append(str(row[Utils.FARE_BASE]))  # Base Fare
        line.append(str(row[Utils.FARE_TAX]))  # TAX TAX TAX
        line.append(str(row[Utils.FARE_MISC]))  # Other Shit
        line.append(str(row[Utils.FARE_TOTAL]))  # Total Amount

        # Write to file
        outputFile.write(printLine(line))

# why does DOW have many numbers?


# Assumptions:
# All fare in USD
