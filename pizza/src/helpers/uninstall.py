import sys 
import subprocess
from .attach import unattach
from core.logger import logger
import os
def uninstall(confirm: bool):
    if confirm:
        unattach()
        exe_path = sys.executable
        cmd = f'cmd /c ping 127.0.0.1 -n 2 > nul & del "{exe_path}"'
        subprocess.Popen(cmd, shell=True)
        os._exit(0)
    else:
        logger.warning("-_-")     