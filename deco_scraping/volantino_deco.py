#ATTENZIONE. Capire come fare questo script!!!!!!!!!!!!
#con questo codice recuperiamo i codici a barre ed i nomi dei prodotti
urls=[
'https://supermercatideco.multicedi.it/static/volantino/volantino-526-0-4.aspx',
'https://supermercatideco.multicedi.it/static/volantino/volantino-533-0-5.aspx',
'https://supermercatideco.multicedi.it/static/volantino/volantino-534-0-6.aspx',
'https://supermercatideco.multicedi.it/static/volantino/volantino-532-0-7.aspx',
'https://supermercatideco.multicedi.it/static/volantino/volantino-531-0-7.aspx'
]


import json
from bs4 import BeautifulSoup
import re
import unidecode
import tor_scraper

def start(prodotto_da_cercare):
    userdata = {}
    print("sto cercando ---> " + prodotto_da_cercare)
    url = prodotto_da_cercare
    print(url)
    html = ''
    while html == '':
        try:
            html = tor_scraper.start_tor(url)
        except:
            html = tor_scraper.start_tor(url)
    soup = BeautifulSoup(html, 'html.parser')

    #userdata['url']='http://'+url

    for row in soup.find('div', class_='col-md-6 descrizionepremio'):
        row=str(row)
        if row.startswith('<h1><span>'):
            cleantext_string=str(row)
            left = '<h1><span>'
            right = '</span>'
            cleantext_string = cleantext_string[cleantext_string.index(left) + len(left):cleantext_string.index(right)]
            userdata['product_name']=cleantext_string
            break

    for i in soup.find_all('div', class_='allergeni'):
        userdata['allergeni']=i.getText().replace('\nAllergeni\r\n','').replace('\n','').strip()

    for i in soup.find_all('div', class_='area_ingredienti'):
        userdata['ingredienti']=i.getText().replace('\nIngredienti\r\n','').replace('\n','').strip()

    for i in soup.find_all(alt="thumb"):
        numbers=[]
        for barcode in i.get('src').split('_'):
            try:
                int(barcode)
                numbers.append(barcode)
            except:
                continue
        userdata['barcode']=max(numbers)
        break

    userdata=str(userdata)+'\n'
    with open("prodotti_deco.txt", "a") as myfile:
        myfile.write(userdata)


a_file = open("link_prodotti_deco.txt", "r")
products_link = a_file.read().splitlines()#[:50]

for link in urls:
    start(link)



