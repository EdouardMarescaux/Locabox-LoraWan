from src.Config import *
import requests
def SendNotificationToMobile( userId:int, title:str, body:str):

    data = {
        "userId": userId,  # Identifiant de l'utilisateur
        "title": title,  # Titre du message
        "body": body  # Contenu du message
    }

    response = requests.post(NOTIFICATION_URL, json=data)  # Envoie la requête POST avec les données JSON
        
    if response.status_code == 200:
        print("✅ Message envoyé avec succès !")
    else:
        print(f"❌ Erreur {response.status_code}: {response.text}")