import ctypes
import tempfile
import os
from core.logger import logger

def set_wallpaper(image_bytes: bytes, extension: str = ".jpg"):
    try:
      with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tmp:
          tmp.write(image_bytes)
          tmp_path = os.path.abspath(tmp.name)
  
      ctypes.windll.user32.SystemParametersInfoW(20, 0, tmp_path, 3)
    except Exception as e:
        logger.error(e)