from src.Config import NOTIFICATION_URL, messages
import requests

def SendNotificationToMobile(userId: int, event: str):
    """
    Envoie une notification push en fonction d'un événement.

    :param userId: ID de l'utilisateur recevant la notification.
    :param event: Clé de l'événement dans `messages` (ex: "box_opened", "intrusion").
    """
    if event not in messages:
        print(f"⚠️ Erreur : L'événement '{event}' n'existe pas dans messages.")
        return False

    title, body = messages[event]  # Récupère le titre et le message associés à l'événement

    data = {
        "userId": userId,
        "title": title,
        "body": body,
    }
    response = requests.post(NOTIFICATION_URL, json=data, timeout=5)

    if response.status_code == 200:
        print(f"✅ Notification '{event}' envoyée avec succès à {userId} !")
        return True
    else:
        print(f"❌ Erreur {response.status_code} : {response.text}")
        return False