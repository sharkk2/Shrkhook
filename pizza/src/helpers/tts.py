import comtypes.client
import threading
from core.logger import logger
import pythoncom

def _speak_tts(text: str):
    try:
      pythoncom.CoInitialize()
      voice = comtypes.client.CreateObject("SAPI.SpVoice")
      voice.Speak(text)
    except Exception as e:
      logger.error(e)    
    finally:
      pythoncom.CoUninitialize()    


def speak_tts(text: str):
    threading.Thread(target=_speak_tts, args=(text,)).start()    
    
    