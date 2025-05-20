import win32gui
import win32process
import psutil

def currentWindow() -> psutil.Process:
    hwnd = win32gui.GetForegroundWindow()
    if hwnd == 0: # tf is hwnd?? "window handle"
        return None
    t, pid = win32process.GetWindowThreadProcessId(hwnd)
    try:
        pro = psutil.Process(pid)
        print(pro.username())
        return pro
    except psutil.NoSuchProcess:
        return None

def getFgs() -> list[psutil.Process]:
     processs = []
     def callback(hwnd, t):
        if win32gui.IsWindowVisible(hwnd):
            try:
                t, pid = win32process.GetWindowThreadProcessId(hwnd)
                pro = psutil.Process(pid)
                if pro not in processs:
                    processs.append(pro)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

     win32gui.EnumWindows(callback, None)
     return processs


def processes() -> list[psutil.Process]:
    processsss = []
    for pro in psutil.process_iter(['pid', 'name', 'username']):
        try:
            processsss.append(pro)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return processsss

def getProcess(name: str) -> psutil.Process:
    for pro in psutil.process_iter(['pid', 'name', 'username']):
        try:
            if pro.name() == name:
                return pro
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return None

def fetchProcess(pid: int) -> psutil.Process: 
    try:
         pro = psutil.Process(pid)
         return pro
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return None
