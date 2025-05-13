import ctypes
import threading

def _show_notification(title, msg, type=0):
    """Show a windows notification
       Types: 
          0: INFO,
          1: WARNING,
          2: QUESTION,
          3: ERROR,
          4: NONE
    """
    
    notf = {
        0: 0x40,
        1: 0x30,
        2: 0x20,
        3: 0x10,
        4: 0
    }
    if type not in notf:
        raise ValueError("Invalid notification type!")           
    
          
    MessageBox = ctypes.windll.user32.MessageBoxW 
    MessageBox(None, f"{msg}", f"{title}", notf[type])   
    
def show_notification(title, msg, type=0):   
    threading.Thread(target=_show_notification, args=(title, msg, type)).start()    
    
