import comtypes.client
import threading

def _speak_tts(text: str):
    voice = comtypes.client.CreateObject("SAPI.SpVoice")
    voice.Speak(text)


def speak_tts(text: str):
    threading.Thread(target=_speak_tts, args=(text,)).start()    
    
    