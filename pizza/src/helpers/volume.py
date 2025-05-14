from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from core.logger import logger

def set_volume(percent: int):  
    try:
      devices = AudioUtilities.GetSpeakers()
      interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
      volume = cast(interface, POINTER(IAudioEndpointVolume))
      volume.SetMasterVolumeLevelScalar(percent / 100.0, None)
    except Exception as e:
        logger.error(e)  