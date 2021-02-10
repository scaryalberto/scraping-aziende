import subprocess as sp
import time

extProc = sp.Popen(['python','remove_rows_and_scraping.py']) # runs myPyScript.py
time.sleep(1200)#2 hours
print("fine primo giro")
sp.Popen.terminate(extProc) # closes the process
extProc = sp.Popen(['python','remove_rows_and_scraping.py']) # runs myPyScript.py
time.sleep(1200)#2 hours
print("fine secondo giro")
sp.Popen.terminate(extProc) # closes the process
extProc = sp.Popen(['python','remove_rows_and_scraping.py']) # runs myPyScript.py
