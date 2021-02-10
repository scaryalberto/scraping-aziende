import requests
from bs4 import BeautifulSoup


def getdata(url):
    r = requests.get(url)
    return r.text

def get_image_from_website(url, single_barcode):
    htmldata = getdata(url)
    soup = BeautifulSoup(htmldata, 'html.parser')

    for idx, item in enumerate(soup.find_all(class_="swiper-slide")):
        if idx==4:
            return
        item = item.find('img')
        indice=item.get('data-index')
        #image_name=''
        if indice=='1':
            image_name='_front'
        if indice=='2':
            image_name='_back'
        if indice=='3':
            image_name='_right'
        if indice=='4':
            image_name='_left'

        url_image="https://www.carrefour.it"+item.get('data-src')
        response = requests.get(url_image)
        image_name=single_barcode+image_name
        file = open(image_name, "wb")#dobbiamo recuperare noi la estensione #creare una cartella dove salvare tutti i file pagina per pagina
        file.write(response.content)
        file.close()




barcodes=["8000070038028","8003753973845","8001685122379","8000070036246"]
for i in barcodes:
    url="https://www.carrefour.it/p/"+i+".html"
    try:
        get_image_from_website(url, i)
    except:
        continue



