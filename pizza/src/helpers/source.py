import hashlib
import json
import base64
import os
from .hardware import get_os

def enc(data: dict, passwrd): # xor
    key = hashlib.sha256(passwrd.encode()).digest()
    raw = json.dumps(data).encode()
    encrypted = bytes([b ^ key[i % len(key)] for i, b in enumerate(raw)])
    return base64.urlsafe_b64encode(encrypted).decode()

def dec(data: str, passwrd):
    key = hashlib.sha256(passwrd.encode()).digest()
    enc = base64.urlsafe_b64decode(data)
    decrypted = bytes([b ^ key[i % len(key)] for i, b in enumerate(enc)])
    return json.loads(decrypted.decode())


def write(data: str):
    user = get_os().get("current_user")
    shark = os.path.join(f"C:/Users/{user}/", ".sharkk2") # ? python micrsoft store version sandboxes appdata for some fucking reason
    os.makedirs(shark, exist_ok=True)
    dat = os.path.join(shark, "sources.shrk")
    with open(dat, "w", encoding="utf-8") as f:
        f.write(data)

def read():
    user = get_os().get("current_user")
    shark = os.path.join(f"C:/Users/{user}/", ".sharkk2") 
    dat = os.path.join(shark, "sources.shrk")
    if not os.path.exists(dat):
        return None
    with open(dat, "r", encoding="utf-8") as f:
        return f.read()