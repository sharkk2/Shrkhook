import time
import pyautogui
import keyboard
import threading

pyautogui.FAILSAFE = False

def _type(text, wpm, enter):
    w_wpm = wpm
    spw = 4 / w_wpm 
    for char in text: 
        if keyboard.is_pressed('esc'):
          break     
        pyautogui.write(char, interval=spw)  
        time.sleep(spw)
    if enter:
        pyautogui.press('enter')     


def type(text, wpm=100, enter=False):
    threading.Thread(target=_type, args=(text, wpm, enter)).start()    
    

