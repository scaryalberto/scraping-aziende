import os
import sys
import time
import subprocess as sp
import telegram_bot


while True:
    my_file = open("demofile1.txt", "r")
    urls = my_file.readlines()
    mancano = len(set(urls))
    message = 'Mancano ancora ' + str(mancano) + ' prodotti da analizzare'
    telegram_bot.telegram_bot_sendtext(message)
    print("fine giro")
    my_file = open("/home/alberto/PycharmProjects/kinder/panomara/demofile1.txt", "r")
    urls = my_file.readlines()
    my_file.close()
    if len(urls) == 0:
        sys.exit()
    extProc = sp.Popen(['python', 'get_pam_products.py'])  # runs myPyScript.py
    status = sp.Popen.poll(extProc)  # status should be 'None'
    time.sleep(3600)
    sp.Popen.terminate(extProc)  # closes the process
    status = sp.Popen.poll(extProc)  # status should now be something other than 'None' ('1' in my testing)
    time.sleep(60)