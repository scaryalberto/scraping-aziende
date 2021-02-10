import json
from bs4 import BeautifulSoup
import re
import unidecode
import tor_scraper
from multiprocessing import Pool
import sys
import os

def start(prodotti_da_cercare):
    i = prodotti_da_cercare
    userdata = {}
    print(": sto cercando ---> " + i)
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

    return userdata


def scraper(lines_to_work):
    prodotti_da_cercare = lines_to_work
    agents = 16
    chunksize = 1
    lista = []
    with Pool(processes=agents) as pool:
        result = pool.map(start, prodotti_da_cercare, chunksize)
        lista.append(result)
        with open('da passare a Claudio1.json', 'a') as file:
            json.dump(lista, file)

#questo blocco di codice prende una serie di righe, le rimuove dal file originale, e ci lavora sopra (forse protrei fare un dag apposito
def remove_row():#il task è lui
    a_file = open("file di appoggio.txt", "r")
    all_lines_of_file = a_file.read().splitlines()
    if len(all_lines_of_file)==0:
        os.remove("file di appoggio.txt")
        sys.exit()
    else:#questa esecuzione ndeve durare 90 minuti, altrimenti kill e riavvi
        lines_to_work = all_lines_of_file[:100]  # change number
        a_file.close()
        my_list = set(all_lines_of_file).difference(lines_to_work)
        with open('file di appoggio.txt', 'w') as f:
            for item in my_list:
                f.write("%s\n" % item)
            f.close
        scraper(lines_to_work)
        remove_row()#richiama la funzione ricorsivamente


remove_row()


