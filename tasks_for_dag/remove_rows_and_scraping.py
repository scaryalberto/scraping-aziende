import json
from bs4 import BeautifulSoup
import re
import unidecode
import tor_scraper
from multiprocessing import Pool
import sys
import os
import time
import telegram_bot

def start(prodotti_da_cercare):
    i = prodotti_da_cercare
    userdata = {}
    print(": sto cercando ---> " + i)
    i = unidecode.unidecode(i)
    i = " ".join(re.findall("[a-zA-Z]+", i))
    url = "https://www.informazione-aziende.it/Azienda_" + i.replace(" ", "_").upper()
    #print(url)
    html = ''
    counter=0
    while html == '' and counter<5:
        try:
            html = tor_scraper.start_tor(url)
        except:
            counter += 1
            html = tor_scraper.start_tor(url)
    soup = BeautifulSoup(html, 'html.parser')
    userdata['manufacturer'] = i
    for link in soup.findAll(class_="title", itemprop="isicV4"):
        result = re.search('>(.*) -', str(link))
        #print(result.group(1))
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
        try:
            result = pool.map(start, prodotti_da_cercare, chunksize)
            lista.append(result)
            with open('da passare a Claudio1.json', 'a') as file:
                json.dump(lista, file)
        except:
            return

#questo blocco di codice prende una serie di righe, le rimuove dal file originale, e ci lavora sopra (forse protrei fare un dag apposito
def remove_row():#il task è lui
    import datetime
    a = datetime.datetime.now()
    message="Orario nuovo for loop => %s" % a
    telegram_bot.telegram_bot_sendtext(message)
    a_file = open("file di appoggio.txt", "r")
    all_lines_of_file = a_file.read().splitlines()
    if len(all_lines_of_file)==0:
        os.remove("file di appoggio.txt")
        telegram_bot.telegram_bot_sendtext("Finitooooooooooooooooooooooooooooooooooooo!")
        sys.exit()
    else:#questa esecuzione ndeve durare 90 minuti, altrimenti kill e riavvi
        lines_to_work = all_lines_of_file[:200]  # change number
        a_file.close()
        my_list = set(all_lines_of_file).difference(lines_to_work)
        with open('file di appoggio.txt', 'w') as f:
            for item in my_list:
                f.write("%s\n" % item)
            f.close
        start_time = time.time()
        scraper(lines_to_work)
        rimangono=len(all_lines_of_file)
        message="concluso il gruppo in: "+ " %.2s minuti " % ((time.time() - start_time)/60)+ "rimangono "+str(rimangono)+ " aziende da analizzare"
        telegram_bot.telegram_bot_sendtext(message)
        remove_row()#richiama la funzione ricorsivamente



remove_row()


