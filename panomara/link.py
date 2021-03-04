#get link for panorama products and download images and descriptions. In a second moment with the image we find the barcode
#in this script we found recursevly all producst link

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import os

def scraper(url):
    req = Request(url)
    html_page = urlopen(req)
    soup = BeautifulSoup(html_page, "lxml")

    for link in soup.findAll('a'):
        link=link.get('href')
        #if link.startswith('/prodotto'):
        #prendi tutti i link ricorsivamente
        link='https://pamacasa.pampanorama.it'+link+'\n'
        if link.startswith('https://pamacasa.pampanorama.ithttps://pamacasa.pampanorama.it/'):
            link=link.replace("https://pamacasa.pampanorama.ithttps://pamacasa.pampanorama.it","https://pamacasa.pampanorama.it")
        try:
            f = open("demofile1.txt", "r")
            if link not in f.readlines():
                f = open("demofile1.txt", "a")
                f.write(link)
                f.close()
            else:
                print("CI STAAAAA")
        except:
            continue
    #os.system("python /home/alberto/PycharmProjects/kinder/panomara/link.py")



import random




if __name__ == '__main__':
    while(True):
        try:
            f = open("demofile1.txt", "r")
            set_url=set(f.readlines())
            url=random.choice(list(set_url))
            scraper(url)
        except:
            url="https://pamacasa.pampanorama.it"
            scraper(url)



