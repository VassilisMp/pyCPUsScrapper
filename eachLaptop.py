import csv
import json
import random
import re
import time

import requests
from bs4 import BeautifulSoup

with open('laptopLinks.json', 'r') as linksFile:
    links = linksFile.read()
links = json.loads(links)
laptops = []

with open('laptops.json', 'r') as lapsFile:
    lapsJson = lapsFile.read()

laptops = json.loads(lapsJson)

# 155
x = 157


def scrap_data(x):
    global laptop
    for i in range(x, len(links) - 1):
        print(links[i]['link'])
        r = requests.get(links[i]['link'])
        soup = BeautifulSoup(r.content, 'html5lib')
        # print(soup.prettify())
        print("Request OK")
        print('{} of {}'.format(i+1, len(links)))

        specGroups = soup.find('div', attrs={'class': 'spec-groups'})
        # soup.find('h1', attrs={'class': 'spec-groups'})

        cpuSpecDetails = specGroups.find('h3', text='Επεξεργαστής (CPU)').parent
        cpuFamily = cpuSpecDetails.find('dt', text='Οικογένεια').parent.dd.span.text
        cpuModel = cpuSpecDetails.find('dt', text='Μοντέλο').parent.dd.span.text

        ramSpecDetails = specGroups.find('h3', text='Μνήμη (RAM)').parent
        ramSize = ramSpecDetails.find('dt', text='Χωρητικότητα Μνήμης').parent.dd.span.text
        ramType = ramSpecDetails.find('dt', text='Τύπος').parent.dd.span.text

        gpuSpecDetails = specGroups.find('h3', text='Κάρτα Γραφικών').parent
        gpuModel = gpuSpecDetails.find('dt', text='Μοντέλο').parent.dd.span.text

        hdd1SpecDetails = specGroups.find('h3', text='Σκληρός Δίσκος').parent
        hdd1Type = hdd1SpecDetails.find('dt', text='Τύπος').parent.dd.span.text
        hdd1Size = hdd1SpecDetails.find('dt', text='Χωρητικότητα').parent.dd.span.text

        hdd2SpecDetails = specGroups.find('h3', text='Δευτερεύων Σκληρός Δίσκος').parent
        hdd2Type = hdd2SpecDetails.find('dt', text='Τύπος').parent.dd.span.text
        hdd2Size = hdd2SpecDetails.find('dt', text='Χωρητικότητα').parent.dd.span.text

        price = links[i]["price(\u20ac)"]

        laptop = {'cpuFamily': cpuFamily,
                  'cpuModel': cpuModel,
                  'ramSize': ramSize,
                  'ramType': ramType,
                  'gpuModel': gpuModel,
                  'hdd1Type': hdd1Type,
                  'hdd1Size': hdd1Size,
                  'hdd2Type': hdd2Type,
                  'hdd2Size': hdd2Size,
                  'price': price
                  }
        laptops.append(laptop)
        time.sleep(random.randrange(2, 5, 1))


scrap_data(155)

jsonStr = json.dumps(laptops, indent=2)
# print(json.loads(jsonStr))
with open('laptops.json', 'w') as laptopsFile:
    laptopsFile.write(jsonStr)

filename = 'laptops.csv'
with open(filename, 'w') as f:
    w = csv.DictWriter(f, ['cpuFamily', 'cpuModel', 'ramSize', 'ramType', 'gpuModel', 'hdd1Type', 'hdd1Size',
                           'hdd2Type', 'hdd2Size', 'price'], delimiter=';')
    w.writeheader()
    for laptop in laptops:
        w.writerow(laptop)

