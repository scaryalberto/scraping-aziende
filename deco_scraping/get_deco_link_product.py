from selenium import webdriver
from bs4 import BeautifulSoup


driver = webdriver.Firefox(executable_path="/home/alberto/PycharmProjects/kinder/deco_scraping/geckodriver")
#to maximize the browser window
#driver.maximize_window()
#get method to launch the URL
driver.get("https://supermercatideco.multicedi.it/static/prodotti/prodottideco.aspx")
#to refresh the browser
import time

time.sleep(5)

# identifying the source element
id = "cookiePopup"
xpath="/html/body/div[3]/div/button[1]"
source= driver.find_element_by_xpath(xpath)
source.click()

for i in range(50):
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    try:
        #source=driver.find_element_by_xpath('//*[@id="pagination"]/li[12]/a')
        source=driver.find_element_by_css_selector(".next")
    except:
        source=driver.find_element_by_xpath('//*[@id="pagination"]/li[18]/a')
    source.click()
    html=driver.page_source
    soup = BeautifulSoup(html)

    for i in soup.find_all('a'):
        url = i.get('href')
        print(url)
        try:

            if url.startswith('/static/prodotto/'):
                url='supermercatideco.multicedi.it'+url+'\n'
                with open("link.txt", "a") as myfile:
                    myfile.write(url)
        except:
            continue
driver.close()
print('fatto!!')

'''
# action chain object creation
action = ActionChains(driver)
# right click operation and then perform
action.context_click(source).perform()
#to close the browser
driver.close()
'''