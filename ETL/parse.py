import csv
notToInclude = {2,3,4,7} #columns not to include
with open("pricing.csv", "rb") as f:
	with open("modified.csv", "w") as f1:
		reader = csv.reader(f, delimiter=",")
		for i, line in enumerate(reader):
			for j in range(len(line)):
				if j in notToInclude: continue #skip these columns
				if j==5: #ORIG
					f1.write("orig" + ',')#replace with mapping to city/country name
				if j==6: #DEST
					f1.write("dest" + ',')#replace with mapping to city/country name
				if j==8: #class need to map to 1,2,3. Y-Economy, what is business and first?
					f1.write("class" + ',')
				else:
					f1.write(line[j] + ',')
			f1.write('\n')


#why does DOW have many numbers?


#Assumptions:
#All fare in USD
