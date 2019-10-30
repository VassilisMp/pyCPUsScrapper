import csv
import pandas as pd

cpuList = list(pd.read_csv("cpus.csv").T.to_dict().values())

# cpuList = []
# filename = 'cpus.csv'

# with open(filename) as csvfile:
#    reader = csv.DictReader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
#    for row in reader:
#        cpuList.append(row)


def filterCPUs(thisrow) -> bool:
    return (thisrow['CPU Value'] > 25) & (thisrow['Category'] == 'Laptop')


filter(filterCPUs, cpuList)
