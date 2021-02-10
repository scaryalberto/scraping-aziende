import json
from bs4 import BeautifulSoup
import re
import unidecode
import tor_scraper
from multiprocessing import Pool

def start(prodotti_da_cercare, counter=[0]):
    counter[0] += 1*16#vediamo quante volte passiamo per questo metodo
    i = prodotti_da_cercare
    userdata = {}
    print(counter, ": sto cercando ---> " + i)
    i = unidecode.unidecode(i)
    i = " ".join(re.findall("[a-zA-Z]+", i))
    url = "https://www.informazione-aziende.it/Azienda_" + i.replace(" ", "_").upper()
    print(url)
    html = ''
    while html == '':
        try:
            html = tor_scraper.start_tor(url)
        except:
            html = tor_scraper.start_tor(url)
    soup = BeautifulSoup(html, 'html.parser')
    userdata['manufacturer'] = i
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

    with open('da passare a Claudio.json', 'a') as file:
        json.dump(userdata, file)
        file.close()


if __name__ == "__main__":
    prodotti_da_cercare = []
    with open("missing_address_difference_for_me.csv") as f:#prossimo file-> aziende2.csv
        for row in f:
            prodotti_da_cercare.append(row.split(";")[0])

            # Run this with a pool of 5 agents having a chunksize of 3 until finished
    prodotti_da_cercare=prodotti_da_cercare[:20000]
    agents = 16
    chunksize = 1
    with Pool(processes=agents) as pool:
        result = pool.map(start, prodotti_da_cercare, chunksize)
    f.close()