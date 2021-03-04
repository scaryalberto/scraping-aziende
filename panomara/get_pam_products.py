#codice per trovare i  codici a barre dei prodotti di PAM
from pyzbar.pyzbar import decode
import cv2
from selenium import webdriver
import urllib.request
#import telegram_bot
import signal, time


class TimeoutError (RuntimeError):
    pass

def handler (signum, frame):
    raise TimeoutError()




def scraper(urls):
    urls = urls
    #link="https://pamacasa.pampanorama.it/spesa-ritiro-negozio/galleria-san-carlo-15/prodotto/sanpellegrino-acq-gas-spellegrino-100-cl-x-6-521584"
#    telegram_bot.telegram_bot_sendtext(message)

    driver = webdriver.Firefox(executable_path="/home/alberto/PycharmProjects/kinder/deco_scraping/geckodriver")

    signal.signal(signal.SIGALRM, handler)

    for link in urls:
        if '/prodotto/' not in link:
            continue
        try:
            signal.alarm(30)  # dopo quanti secondi scatta il timer

            if link.startswith('https://pamacasa.pampanorama.ithttps://pamacasa.pampanorama.it/prodotto/'):
                link=link.replace('https://pamacasa.pampanorama.ithttps://pamacasa.pampanorama.it/prodotto/', 'https://pamacasa.pampanorama.it/prodotto/')
            print(link)

            try:
                driver.get(link.replace('\n',''))
            except:
                driver.get(link)

            time.sleep(5)

            # get the image source
            for n in range(1,10):
                try:
                    img=driver.find_element_by_css_selector(".main-thumb-ul > li:nth-child({number}) > img:nth-child(1)".format(number=n))
                    src = img.get_attribute('src')
                    src=src.replace('.jpg&w=300&h=280', '.jpg&w=500&h=500')
                    # download the image
                    urllib.request.urlretrieve(src, "local-filename.png")
                    img = cv2.imread("local-filename.png")
                    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    barcodes = decode(gray_img)
                    barcode = barcodes[0].data
                    print(barcode)

                    #ingredienti e allergeni
                    submit_button = driver.find_element_by_css_selector(".accordion > li:nth-child(1) > h3:nth-child(1)")
                    submit_button.click()

                    try:
                        text = driver.find_element_by_css_selector(".open > div:nth-child(2) > div:nth-child(1)")
                        ingredients=text.text.split('\n')
                    except:
                        ingredients='nessuno'

                    try:
                        text = driver.find_element_by_css_selector("div.acc - block: nth - child(2)")
                        allergens=text.text.split('\n')
                    except:
                        allergens='nessuno'

                    #nome
                    text = driver.find_element_by_css_selector(".popup-product-info > div:nth-child(1) > h2:nth-child(1)")
                    product_name=text.text

                    #brand
                    text = driver.find_element_by_css_selector(
                        "div.product-info:nth-child(1) > div:nth-child(2) > span:nth-child(1)")
                    brand=text.text

                    userdata={'url': link.replace('\n',''),
                     'product_name': product_name, 'allergeni': allergens, 'ingredienti': ingredients,
                     'barcode': barcode}
                    userdata = str(userdata) + '\n'
                    with open("prodotti_pam.txt", "a") as myfile:
                        myfile.write(userdata)

                    driver.quit()
                    break


                except:
                    driver.quit()
                    continue



        except TimeoutError as ex:
            print('timeout', link)
            driver.quit()
            continue




if __name__ == "__main__":
    while True:

        my_file = open("demofile1.txt", "r")
        urls = my_file.readlines()
        mancano = len(urls)
        message = 'Mancano ancora ' + str(mancano) + ' prodotti da analizzare'
        urls=list(set(urls))
        if len(urls)>0:
            try:
                n=10
                scraper(urls[:n])
                urls_da_togliere=urls[:n]
                difference=(set(urls) - set(urls_da_togliere))
                print("cancellato dei prodotti dalla lista")

                with open('demofile1.txt', 'w') as f:
                    for item in difference:
                        f.write("%s\n" % item)




            except:
                import os
                os.system('python get_pam_products.py')
        else:
            import sys
            sys.exit()