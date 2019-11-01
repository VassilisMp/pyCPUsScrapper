# Python program to scrape website
# and save quotes from website
import requests
from bs4 import BeautifulSoup
import csv
import re

# URL = "https://www.cpubenchmark.net/cpu_list.php"
URL = "https://www.cpubenchmark.net/CPU_mega_page.html"

r = requests.get(URL)
print("Request OK")

soup = BeautifulSoup(r.content, 'html5lib')

cpus = []  # a list to store quotes

# trs = soup.find('table', attrs={'id': 'cputable'}).find('tbody').find_all('tr')
trs = soup.find('table', attrs={'id': 'cputable'}).find('tbody').find_all('tr', id=re.compile("cpu.*"))


regex = re.compile(r".(\d+\.\d+).")
for row in trs:
    try:
        price = float(regex.match(row.contents[1].text).group(1))
    except AttributeError:
        price = 0
    try:
        mark = int(row.contents[2].text)
    except ValueError:
        mark = 0
    try:
        val = float(row.contents[3].text)
    except ValueError:
        val = 0
    try:
        threadMark = int(row.contents[4].text)
    except ValueError:
        threadMark = 0
    try:
        threadVal = float(row.contents[5].text)
    except ValueError:
        threadVal = 0
    try:
        tdp = int(row.contents[6].text)
    except ValueError:
        tdp = 0
    try:
        powerPerf = int(row.contents[7].text)
    except ValueError:
        powerPerf = 0

    cpu = {'CPU Name': row.contents[0].text,
           'Price(USD)': price,
           'CPU Mark': mark,
           'CPU Value': val,
           'Thread Mark': threadMark,
           'Thread Value': threadVal,
           'TDP (W)': tdp,
           'Power Perf.': powerPerf,
           'Socket': row.contents[9].text,
           'Category': row.contents[10].text
           }
    cpus.append(cpu)

filename = 'cpus.csv'
with open(filename, 'w') as f:
    w = csv.DictWriter(f, ['CPU Name', 'Price(USD)', 'CPU Mark', 'CPU Value', 'Thread Mark', 'Thread Value', 'TDP (W)',
                           'Power Perf.', 'Socket', 'Category'], delimiter=';')
    w.writeheader()
    for cpu in cpus:
        w.writerow(cpu)
