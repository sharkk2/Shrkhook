import os
import sys
import config
import win32com.client
from core.logger import logger
import winreg

def isDisabled():
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\StartupFolder"
        )
        value, regtype = winreg.QueryValueEx(key, f"{config.attach_shortcut_name}.lnk")
        winreg.CloseKey(key)
        # first byte = 0x03 = disabled else enabled (0x02 or just not existing)
        return value[0] == 3
    except FileNotFoundError:
        return False  
    except Exception as e:
        logger.error(f"Failed to check startup status: {e}")
        return None


def enable():
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\StartupFolder",
            0,
            winreg.KEY_SET_VALUE
        )
        
        # first byte 0x02 = enabled
        # i hope i don't fck up something critical when testing this
        envalue = b'\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

        winreg.SetValueEx(key, f"{config.attach_shortcut_name}.lnk", 0, winreg.REG_BINARY, envalue)
        winreg.CloseKey(key)
        return True
    except Exception as e:
        return False

def attach():
    if isAttached():
        logger.warning("Attach status is already true")
        return False, "Attach status is already true"

    logger.info("Attempting attach")
    try:
        exe = sys.executable
        startup_folder = os.path.join(
            os.environ["APPDATA"],
            r"Microsoft\Windows\Start Menu\Programs\Startup"
        )
        shortcut_path = os.path.join(startup_folder, f"{config.attach_shortcut_name}.lnk")

        if os.path.exists(shortcut_path):
            if isDisabled():
              enable()
              logger.info("Attach successful! I'm attached to startup")
              return True, ""
            else: 
              os.remove(shortcut_path)
              logger.info("Attacher found and deleted a zombie shortcut")

        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(shortcut_path)
        shortcut.TargetPath = exe
        shortcut.WorkingDirectory = os.path.dirname(exe)
        shortcut.IconLocation = "shell32.dll,0"
        shortcut.Arguments = "--startup"
        shortcut.IconLocation = exe
        shortcut.Save()

        logger.info("Attach successful! I'm attached to startup")
        return True, ""
    except Exception as e:
        logger.error(f"Attach failed: {e}")
        return False, e
    
    
def isAttached():
    startup_folder = os.path.join(
        os.environ["APPDATA"],
        r"Microsoft\Windows\Start Menu\Programs\Startup"
    )
    shortcut_path = os.path.join(startup_folder, f"{config.attach_shortcut_name}.lnk")
    if not os.path.exists(shortcut_path):
        return False
    
    if isDisabled():
        return False

    exe = sys.executable
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(shortcut_path)
    return os.path.abspath(shortcut.TargetPath) == os.path.abspath(exe)