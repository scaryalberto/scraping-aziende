#in questo script vado a prendere le aziende dove già già ho il link
import json
from bs4 import BeautifulSoup
import re
import tor_scraper

prodotti_da_cercare = []
lista = []

with open("aziende con link.csv") as f:
    for row in f:
        try:
            nome=row.split(";")[0]
            url = row.split(";")[1]

            userdata = {}
            print(url)
            html = ''
            while html == '':
                try:
                    html = tor_scraper.start_tor(url)
                except:
                    html = tor_scraper.start_tor(url)
            soup = BeautifulSoup(html, 'html.parser')
            userdata['manufacturer'] = nome
            for link in soup.findAll(class_="title", itemprop="isicV4"):
                result = re.search('>(.*) -', str(link))
                print(result.group(1))
                userdata['ateco'] = result.group(1)

            for i in soup.findAll(class_="locality", itemprop="addressLocality"):
                userdata['city'] = i.getText()

            for i in soup.findAll(class_="postal-code", itemprop="postalCode"):
                userdata['zipCode'] = i.getText()

            for i in soup.findAll(class_="street-address", itemprop="streetAddress"):
                userdata['address'] = i.getText()

            for i in soup.findAll(class_="url", itemprop="url"):
                userdata['website'] = i.get("href")

            lista.append(userdata)

        except:
            continue

f.close()

with open('result1.json', 'w') as file:
    json.dump(lista, file)

print("ECCOMIIIIIIII")