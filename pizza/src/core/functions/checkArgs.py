import sys
from qr_code import start as startQR
import threading

def checkArgs():
    if "--startup" not in sys.argv:
        threading.Thread(target=startQR).start()    
