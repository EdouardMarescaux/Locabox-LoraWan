import requests
# from src.Config import NOTIFICATION_URL, messages  # Assure-toi que MESSAGES est défini dans Config.py
from src.Config import *
def SendNotificationToMobile(user_id: int, event: str):
    """Envoie une notification à l'utilisateur via une API de notification."""
    
    # Convertir l'événement en minuscule pour éviter des problèmes de casse
    event = event.lower()

    # Vérifier si l'événement est défini dans le dictionnaire MESSAGES
    if event not in messages:
        print(f"Erreur : L'événement '{event}' n'existe pas dans MESSAGES.")
        return False  # Empêche l'envoi si l'événement est invalide

    message = messages[event]  # Récupérer le message lié à l'événement
    title = titles[event]  # Récupérer le titre lié à l'événement

    # Construire les données pour l'API
    payload = {
        "userId": user_id,
        "title": title,
        "body": message,
    }

    # Définir les en-têtes de la requête
    headers = {
        "Content-Type": "application/json",  # Spécifie que les données sont en JSON
    }

    try:
        # Envoi de la notification à l'API via une requête POST
        response = requests.post(NOTIFICATION_URL, json=payload, headers=headers, timeout=5)
        # Vérifier la réponse de l'API
        if response.status_code == 200:
            print(f"Notification envoyée avec succès à l'utilisateur {user_id} : {message}")
            return True
        else:
            # Afficher un message d'erreur détaillé en cas de code 400 ou autre
            print(f"Erreur lors de l'envoi de la notification (Code {response.status_code})")
            return False

    except requests.RequestException as e:
        # Si une erreur réseau se produit
        print(f"Erreur réseau lors de l'envoi de la notification : {e}")
        return False