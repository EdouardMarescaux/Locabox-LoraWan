import grpc
from chirpstack_api.as_pb.external import api
from src.Config import *
import random

# Fonction pour générer un code
def generate_code():
    return random.randint(100000, 999999)

# Fonction pour envoyer le code
# def send_code():
#     channel = grpc.insecure_channel(CHIRPSTACK_SERVER)
#     client = api.DeviceQueueServiceStub(channel)

#     auth_token = [("authorization", "Bearer %s" % API_TOKEN)]

#     req = api.EnqueueDeviceQueueItemRequest()
#     req.device_queue_item.confirmed = False
#     req.device_queue_item.data = bytes([0x43, 0x32, 0x31, 0x33, 0x36, 0x35, 0x36, 0x45])
#     req.device_queue_item.dev_eui = dev_eui.hex()
#     req.device_queue_item.f_port = 10

#     resp = client.Enqueue(req, metadata=auth_token)
#     print(f"Code envoyé : données enqueue", resp.f_cnt)

# Fonction pour traiter le message de démarrage
def handle_start_message():
    print("Message de démarrage reçu. Génération d'un code...")
    code = generate_code()
    print(f"Code généré : {code}")
    send_code(code)

# Fonction qui écoute les messages et les traite
def listen_for_messages():
    channel = grpc.insecure_channel(CHIRPSTACK_SERVER)
    client = api.DeviceQueueServiceStub(channel)  # Utilisation de DeviceQueueServiceStub pour interagir avec la queue des messages

    auth_token = [("authorization", "Bearer %s" % API_TOKEN)]

    req = api.GetDeviceQueueRequest()  # Cette ligne devrait être modifiée pour correspondre au bon service

    # Essaye une autre méthode de récupération des messages (par exemple Get ou List)
    # À adapter selon ce qui est disponible dans ton API de Chirpstack
    try:
        resp = client.GetDeviceQueue(req, metadata=auth_token)  # Exemple d'appel (à vérifier avec la vraie méthode)
        
        for message in resp.items:
            if message.payload == b"START":  # Si un message "START" est reçu
                handle_start_message()

    except grpc.RpcError as e:
        print(f"Erreur lors de l'appel à l'API de Chirpstack : {e}")

