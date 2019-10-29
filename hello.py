# Python program to scrape website
# and save quotes from website
import requests
from bs4 import BeautifulSoup
import csv
import re

URL = "https://www.cpubenchmark.net/cpu_list.php"
r = requests.get(URL)
print("Request OK")

soup = BeautifulSoup(r.content, 'html5lib')

cpus = []  # a list to store quotes

trs = soup.find('table', attrs={'id': 'cputable'}).find('tbody').find_all('tr')

regex = re.compile(r".(\d+\.\d+).")
for row in trs:
    try:
        mark = int(row.contents[1].text)
    except ValueError:
        mark = 0
    try:
        rank = int(row.contents[2].text)
    except ValueError:
        rank = 0
    try:
        val = float(row.contents[3].text)
    except ValueError:
        val = 0
    try:
        price = float(regex.match(row.contents[4].text).group(1))
    except AttributeError:
        price = 0
    cpu = {'CPU Name': row.contents[0].a.text,
           'Passmark CPU Mark': mark,
           'Rank': rank,
           'CPU Value': val,
           'Price(USD)': price}
    cpus.append(cpu)

filename = 'cpus.csv'
with open(filename, 'w') as f:
    w = csv.DictWriter(f, ['CPU Name', 'Passmark CPU Mark', 'Rank', 'CPU Value', 'Price(USD)'])
    w.writeheader()
    for cpu in cpus:
        w.writerow(cpu)
