import pandas as pd
from Utils import *
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

def loadStockData():
    stock_dict = {}
    with open("../data/external/dowjonesdiff.csv", "r") as prices:
        for line in prices:
            data = line.split(" ")
            dateOrigFormat = data[0]
            date = datetime.strptime(dateOrigFormat.strip(), "%Y-%m-%d")
            stock_dict[date] = data[1].strip()
    return stock_dict

def loadOilPrices():
    oil_dict = {}
    with open("../data/external/oilPrices2000.csv", "r") as prices:
        for line in prices:
            data = line.split(",")
            dateOrigFormat = data[0]
            date = datetime.strptime(dateOrigFormat.strip(), "%Y-%m-%d")
            oil_dict[date] = data[2].strip()
    return oil_dict

def loadAttackData():
    attack_dict = dict()
    with open("../data/external/attacks.csv", "r") as attacks:
        for line in attacks:
            data = line.split(" ")
            year = data[0]
            month = data[1]
            day = data[2]
            country = data[3].strip()
            dateFormat = year + "-" + month + "-" + day
            if day != "0": #bug in data where some days are 0
              date = datetime.strptime(dateFormat.strip(), "%Y-%m-%d")
              if date in attack_dict:
                attack_dict[date].append(country)
              else:
                attack_dict[date] = [country]
    return attack_dict


def loadAirportData():
    airport_dict = {}
    airports = pd.read_csv("../data/external/airports.csv")
    for i, line in airports.iterrows():
        data = {}
        data[AIRPORT_NUM] = str(line[AIRPORT_NUM])
        data[COUNTRY] = line[COUNTRY]
        data[AIRPORT_COUNTRY_CODE] = line[AIRPORT_COUNTRY_CODE]
        data[AIRPORT_REGION] = line[AIRPORT_REGION]
        airport_dict[line[AIRPORT_CODE]] = data
    return airport_dict
    # To convert the airport code from three letter to ID,
    # simply use, for instance = airport_dict['JFK'][AIRPORT_NUM]


def airportID(airportCode):
    return airport_dict[airportCode][AIRPORT_NUM]


def findClosetOilPrice(date):
    dateTime = datetime.strptime(date, "%m/%d/%y")
    count = 0
    while dateTime not in oil_dict:
        if count > 10:
            return '0.0'  # disregard if older than 10 days
        dateTime -= timedelta(days=1)
        count += 1
    return oil_dict[dateTime]

def findClosetStockDiff(date):
    dateTime = datetime.strptime(date, "%m/%d/%y")
    count = 0
    while dateTime not in stock_dict:
        if count > 100:
            return '0.0'  # disregard if older than 10 days
        dateTime -= timedelta(days=1)
        count += 1
    return stock_dict[dateTime]


def loadDistance():
    distanceDict = {}
    with open("../data/emirates/city-distance.csv", "r") as distances:
        for line in distances:
            arr = line.split(',')
            distanceDict[arr[0].strip()] = str(arr[1].strip())
    return distanceDict

def loadHotelOccupancyData():
    hotelOccupancyDict = dict()
    hotelOccupancyData = pd.read_csv("../data/external/hotelOccupancyRatesMonthlyRegion.csv")
    for i, row in hotelOccupancyData.iterrows():
        data = dict()
        data[ASIA_PACIFIC] = row[ASIA_PACIFIC] / 100.0
        data[AMERICAS] = row[AMERICAS] / 100.0
        data[EUROPE] = row[EUROPE] / 100.0
        data[ME_AFRICA] = row[ME_AFRICA] / 100.0
        date = datetime.strptime(row[HOTEL_OCCUPANCY_DATE], "%m/%d/%y")
        hotelOccupancyDict[date] = data
    return hotelOccupancyDict


def getHotelOccupancy(date, airportCode):
    region = airport_dict[airportCode][AIRPORT_REGION]
    hotelOccupancyDate = datetime(year=date.year, month=date.month, day=1)
    if hotelOccupancyDict.get(hotelOccupancyDate) is None:
        return None
    else:
        return str(hotelOccupancyDict[hotelOccupancyDate][region])


airport_dict = loadAirportData()
oil_dict = loadOilPrices()
stock_dict = loadStockData()
attack_dict = loadAttackData()
hotelOccupancyDict = loadHotelOccupancyData()
distanceDict = loadDistance()

# print distanceDict
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
                  "changeInOilPrice",
                  "terroristAttack",
                  "ChangeInStockIndex",
                  "origHotelOccupancy",
                  "destHotelOccupancy",
                  "distance",
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

        if getHotelOccupancy(departureDate, row[ORIGIN]) is None or getHotelOccupancy(departureDate, row[DESTINATION]) is None:
            continue

        line.append(dayOfWeek(departureDate))
        line.append(isWeekend(departureDate))
        line.append(month(departureDate))
        line.append(travelSpan())
        line.append(marketShare(row[MARKET_SHARE]))
        line.append(airportID(row[ORIGIN]))  # origin
        line.append(airportID(row[DESTINATION]))  # destination
        oilPrice = findClosetOilPrice(row[DEPARTURE_DATE])  # probably need to give purchase date?
        line.append(oilPrice)
        country = airport_dict[row[DESTINATION]][COUNTRY]
        attack = "0"
        #TEST
        if departureDate in attack_dict:
          if country in attack_dict[departureDate]:
            attack = "1"
        line.append(attack)
        stockIndexDiff = findClosetStockDiff(row[DEPARTURE_DATE])
        line.append(stockIndexDiff)

        line.append(getHotelOccupancy(departureDate, row[ORIGIN]))
        line.append(getHotelOccupancy(departureDate, row[DESTINATION]))

        distance_key = row[ORIGIN]+':'+row[DESTINATION]
        line.append(distanceDict[distance_key])

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
