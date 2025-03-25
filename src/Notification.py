import requests
def SendNotificationToMobile( userId:int, title:str, body:str):
    # DEST_IP = "172.16.0.30"  # Remplace par l'IP du destinataire
    # PORT = 3000  # Port du serveur
    URL = f"http://172.16.0.30:3000/send-notification"

    data = {
        "userId": userId,  # Identifiant de l'utilisateur
        "title": title,  # Titre du message
        "body": body  # Contenu du message
    }

    response = requests.post(URL, json=data)  # Envoie la requête POST avec les données JSON
        
    if response.status_code == 200:
        print("✅ Message envoyé avec succès !")
    else:
        print(f"❌ Erreur {response.status_code}: {response.text}")