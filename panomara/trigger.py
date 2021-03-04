import os
import sys
import time
import subprocess as sp

while True:
    print("fine giro")
    my_file = open("get_pam_products.py", "r")
    urls = my_file.readlines()
    my_file.close()
    if len(urls) == 0:
        sys.exit()
    extProc = sp.Popen(['python', 'get_pam_products.py'])  # runs myPyScript.py
    status = sp.Popen.poll(extProc)  # status should be 'None'
    time.sleep(600)
    sp.Popen.terminate(extProc)  # closes the process
    status = sp.Popen.poll(extProc)  # status should now be something other than 'None' ('1' in my testing)