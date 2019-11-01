import json
import time

import requests
from bs4 import BeautifulSoup
import csv
import re

URL = "https://www.skroutz.gr/c/25/laptop/f/342316_342323_363862_363863_728946_789315/8GB-SSD-Intel-Core-i5-Intel" \
      "-Core-i7-16GB-12GB.html?o=laptop&order_by=pricevat&order_dir=asc "
skroutzDom = 'https://www.skroutz.gr'
r = requests.get(URL)
print("Request OK")

soup = BeautifulSoup(r.content, 'html5lib')
laptops = []

paginator = soup.find('ol', attrs={'class': 'react-component paginator cf'}).contents

pagesSize = int(paginator[len(paginator)-2].a.getText())
link = skroutzDom + paginator[len(paginator)-2].a.get('href')
link = re.sub(r'\d+$', "", link)

laptopLinks = []

regex = re.compile(r".*?(\d+\.\d+).*")
for i in range(1, pagesSize-1):
    while True:
        try:
            paginator = soup.find('ol', attrs={'class': 'react-component paginator cf'}).contents
            link = skroutzDom + paginator[len(paginator) - 2].a.get('href')
            link = re.sub(r'\d+$', "", link)
            link = link + str(i)
            r = requests.get(link)
            print("page " + str(i) + " request OK")
            soup = BeautifulSoup(r.content, 'html5lib')
            # print(soup.prettify())
            lis = soup.find('ol', attrs={'id': "sku-list"}).find_all('a', attrs={'class': 'js-sku-link sku-link'})
            print(lis)
            for a in lis:
                # print(skroutzDom + a.get('href'))
                # print(a.getText())
                priceText = a.getText().replace('.', '').replace(',', '.')
                # print(priceText)
                # print(regex.match(priceText).group(1))
                price = float(regex.match(priceText).group(1))
                # print(price)
                laptopLinks.append({'link': skroutzDom + a.get('href'), 'price(€)': price})
        except AttributeError:
            continue
        break
jsonStr = json.dumps(laptopLinks, indent=2)
# print(json.loads(jsonStr))
with open('laptopLinks.json', 'w') as linksFile:
    linksFile.write(jsonStr)
