import csv
import json

import pandas as pd

cpuList = list(pd.read_csv("cpus.csv", sep=";").T.to_dict().values())

# cpuList = []
# filename = 'cpus.csv'

# with open(filename) as csvfile:
#    reader = csv.DictReader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
#    for row in reader:
#        cpuList.append(row)


def filterCPUs(thisrow) -> bool:
    return (thisrow['CPU Value'] > 25) & (thisrow['Category'] == 'Laptop')

with open('laptops.json', 'r') as lapsFile:
    lapsJson = lapsFile.read()

laptops = json.loads(lapsJson)
laptops = pd.DataFrame(laptops)
cpuList = pd.read_csv("cpus.csv", sep=";")
ddr4 = laptops[laptops.ramType == 'DDR4']
ddr4['vfm'] = ddr4.cpuModel.apply(lambda x: cpuList[cpuList['CPU Name'].str.contains(x)]['CPU Mark'].values[0])
ddr4['mark'] = ddr4.cpuModel.apply(lambda x: cpuList[cpuList['CPU Name'].str.contains(x)]['CPU Mark'].values[0])
ddr4['TDP'] = ddr4.cpuModel.apply(lambda x: cpuList[cpuList['CPU Name'].str.contains(x)]['TDP (W)'].values[0])



filter(filterCPUs, cpuList)
