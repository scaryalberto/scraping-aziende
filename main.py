import json
from bs4 import BeautifulSoup
import re
import unidecode
import tor_scraper

f = open('parole_da_cercare.txt', 'r')
prodotti_da_cercare = f.read().splitlines()
f.close()

lista=[]
for idx, i in enumerate(prodotti_da_cercare[600:]):
    userdata = {}
    print(idx, ": sto cercando ---> " + i)
    i=unidecode.unidecode(i)
    i = " ".join(re.findall("[a-zA-Z]+", i))
    url = "https://www.informazione-aziende.it/Azienda_" + i.replace(" ", "_").upper()
    print(url)
    html =''
    while html=='':
        try:
            html=tor_scraper.start_tor(url)
        except:
            html = tor_scraper.start_tor(url)
    soup = BeautifulSoup(html, 'html.parser')
    userdata['nome']=i
    for link in soup.findAll(class_="title", itemprop="isicV4"):
        result = re.search('>(.*) -', str(link))
        print(result.group(1))
        userdata['ateco']=result.group(1)

    for i in soup.findAll(class_="locality", itemprop="addressLocality"):
        userdata['city']=i.getText()

    for i in soup.findAll(class_="postal-code", itemprop="postalCode"):
        userdata['cap']=i.getText()

    for i in soup.findAll(class_="street", itemprop="streetAddress"):
        userdata['indirizzo_fisico']=i.getText()

    for i in soup.findAll(class_="url", itemprop="url"):
        userdata['sito_web']=i.get("href")
    
    lista.append(userdata)
    #time.sleep(3)

with open('result7.json', 'w') as file:
    json.dump(lista , file)

print("ECCOMIIIIIIII")