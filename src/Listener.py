# import grpc
# from chirpstack_api.as_pb.external import api
# from src.Config import *
# from src.Codes import *

# # Fonction pour envoyer un code en aval (downlink)
# def send_code(dev_eui, code):
#     channel = grpc.insecure_channel(CHIRPSTACK_SERVER)
#     client = api.DeviceQueueServiceStub(channel)

#     auth_token = [("authorization", "Bearer %s" % API_TOKEN)]

#     req = api.EnqueueDeviceQueueItemRequest()
#     req.device_queue_item.confirmed = False
#     req.device_queue_item.data = code.to_bytes(4, byteorder="big")  # Convertir le code en 4 octets
#     req.device_queue_item.dev_eui = dev_eui
#     req.device_queue_item.f_port = 10  # Port LoRaWAN à utiliser

#     try:
#         resp = client.Enqueue(req, metadata=auth_token)
#         print(f"Code envoyé avec succès : {code}, f_cnt : {resp.f_cnt}")
#     except grpc.RpcError as e:
#         print(f"Erreur lors de l'envoi du code : {e.details()}")

# # Fonction pour traiter le message de démarrage
# def handle_start_message(dev_eui):
#     print("Message de démarrage reçu. Génération d'un code...")
#     code = generate_code()
#     print(f"Code généré : {code}")
#     send_code(dev_eui, code)

# # Fonction qui écoute les messages et les traite
# def listen_for_messages(dev_eui):
#     channel = grpc.insecure_channel(CHIRPSTACK_SERVER)
#     client = api.DeviceServiceStub(channel)  # Utilisation de DeviceServiceStub pour interagir avec les messages

#     auth_token = [("authorization", "Bearer %s" % API_TOKEN)]

#     try:
#         # Exemple : récupérer les messages en attente pour un dispositif
#         req = api.StreamEventLogsRequest(dev_eui=dev_eui)  # Remplacez par le DevEUI de votre ESP32
#         for event in client.StreamEventLogs(req, metadata=auth_token):
#             if event.type == "up" and event.payload == b"DR":  # Vérifie si le message est "DR"
#                 handle_start_message(event.dev_eui)

#     except grpc.RpcError as e:
#         print(f"Erreur lors de l'écoute des messages : {e.details()}")

import json
from src.Codes import *
from src.ESP32 import *
from src.Alarm import *
from src.Acces import *

def listen_from_php_file():
    try:
        with open("message.json", "r") as file:
            message = json.load(file)

        dev_eui = message["dev_eui"]
        payload = message["payload"].strip()

        print(f"[~] Message reçu : {payload} | DevEUI : {dev_eui}")

        # Décision en fonction du message
        if payload == "DC":
            print("[*] Démarrage détecté. Génération et envoi du code.")
            code = generate_code()
            sendCode(dev_eui, code)

        elif payload == "IT":
            print("[!] Intrusion détectée. Traitement de l'alarme.")
            alarm_intrusion()

        elif payload == "OU":
            print("[*] Accès demandé. Ouverture du box.")
            handle_access(1)  # Remplacez par une logique dynamique si nécessaire

        else:
            print(f"[!] Message non reconnu : {payload}")

    except FileNotFoundError:
        print("[!] Aucun message reçu.")
    except json.JSONDecodeError:
        print("[!] Erreur de format JSON.")
