import json
from src.Config import *
from src.Message import *
from src.Alarm import *
from src.Acces import *
from src.ESP32 import *

def listen():
    try:
        with open("message.json", "r") as f:
            message_data = json.load(f)

        dev_eui = message_data["dev_eui"]
        payload = message_data["payload"]

        print(f"[~] Message reçu via webhook : '{payload}' — DevEUI: {dev_eui}")
        parse_and_handle(payload, dev_eui)

    except FileNotFoundError:
        print("[!] Fichier message.json non trouvé.")
    except json.JSONDecodeError:
        print("[!] Erreur lors de la lecture du JSON.")
    except KeyError as e:
        print(f"[!] Clé manquante dans le JSON : {e}")

def parse_and_handle(message: str, dev_eui: str):
    if "IT" in message:
        print("→ Intrusion détectée.")
        alarm_intrusion()
    elif "OK" in message:
        print("→ Accès autorisé.")
        handle_access(1)
    elif "DC" in message:
        print("→ Demande de code détectée.")
        sendCode(dev_eui)
    else:
        print("→ Message non reconnu :", message)

if __name__ == "__main__":
    listen()