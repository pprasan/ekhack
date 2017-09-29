import pandas as pd
from datetime import datetime

pricingDF = pd.read_csv("../data/emirates/pricing.csv")

with open("../data/emirates/parsedPricingData.csv", "w") as outputFile:
    for i, row in pricingDF.iterrows():
        departureDate = datetime.strptime(row["DEPARTURE_DATE"], "%m/%d/%y")
        outputFile.write(str(departureDate.year) +
                         "\n")


# why does DOW have many numbers?


# Assumptions:
# All fare in USD
