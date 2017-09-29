import pandas as pd
from datetime import datetime

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
        departureDate = datetime.strptime(row["DEPARTURE_DATE"], "%m/%d/%y")
        outputFile.write(str(departureDate.year) +
                         "\n")

# why does DOW have many numbers?


# Assumptions:
# All fare in USD
