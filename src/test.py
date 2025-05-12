import grpc
from chirpstack_api.as_pb.external import api
from src.Config import *
from src.Message import *
from src.Alarm import *
from src.Acces import *
from src.ESP32 import *

def listen_and_process(dev_eui: str):
    """Écoute les messages ChirpStack et les interprète via parse_and_handle()."""
    channel = grpc.insecure_channel(CHIRPSTACK_SERVER)
    client = api.DeviceServiceStub(channel)
    auth_token = [("authorization", f"Bearer {API_TOKEN}")]

    try:
        print(f"[~] Connexion à ChirpStack pour écouter les messages du device {dev_eui}...")
        req = api.StreamEventLogsRequest(dev_eui=dev_eui)

        for event in client.StreamEventLogs(req, metadata=auth_token):
            if event.type == "up":
                try:
                    payload = event.payload.decode("utf-8").strip()
                    print(f"[>] Message reçu : '{payload}'")
                    parse_and_handle(payload)  # Interprète le message et déclenche l'action appropriée
                except UnicodeDecodeError:
                    print("[!] Erreur : Payload non décodable (binaire ?)")

    except grpc.RpcError as e:
        print(f"[X] Erreur lors de l'écoute : {e.details()}")

def parse_and_handle(message: str):
    """Analyse le message et déclenche l'action appropriée selon son contenu."""
    if "MOKC" in message:
        # Exemple d'intrusion (par exemple "MOKC AITE BOUS")
        print("Intrusion détectée !")
        alarm_intrusion()  # Appel à la gestion d'intrusion
    elif "OK" in message:
        # Exemple d'ouverture de box (par exemple "MOKC AITE BOUS")
        print("Accès autorisé. Ouverture de la box.")
        handle_access(1)  # Ouverture de la box 1 (remplacez par l'ID réel)
    elif "DR" in message:
        # Exemple de démarrage (envoie d'un code)
        print("Démarrage reçu. Envoi d'un code.")
        sendCode()  # Envoi du code via ESP32

if __name__ == "__main__":
    # Remplace par ton vrai DevEUI
    listen_and_process(dev_eui)
