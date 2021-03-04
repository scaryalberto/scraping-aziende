import signal, time, random

class TimeoutError (RuntimeError):
    pass

def handler (signum, frame):
    raise TimeoutError()

signal.signal (signal.SIGALRM, handler)

for i in range(5):
    try:
        signal.alarm (10)#dopo quanti secondi scatta il timer

    except TimeoutError as ex:
        print ('timeout', i)
        continue