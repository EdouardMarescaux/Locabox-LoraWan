import mysql.connector
from src.Notification import *
from src.Config import *

def alarm_intrusion():
    """Surveille la base de données pour détecter une intrusion et envoyer une notification."""

    try:
        with mysql.connector.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                # Recherche d'une intrusion non encore notifiée
                cursor.execute("""
                    SELECT alarm_log.alarm_date, alarm_log.id_box, id_user_box, LOWER(info) 
                    FROM alarm_log 
                    JOIN rent ON rent.id_box = alarm_log.id_box 
                    WHERE alarm_log.notify = 0 AND info = 'intrusion' 
                    LIMIT 1;
                """)
                result = cursor.fetchone()

                if not result:
                    return  # Rien à notifier

                alarm_date, id_box, id_user, info = result

                print(f"Intrusion détectée sur la box {id_box}. Envoi de notification...")

                # Vérifie que l'événement est bien dans le dictionnaire des messages
                if info in messages:
                    if SendNotificationToMobile(id_user, info):
                        # Mise à jour de la notification après succès
                        update_notification_status(alarm_date)
                else:
                    print(f"Erreur : L'événement '{info}' n'existe pas dans messages.")

    except mysql.connector.Error as err:
        print(f"Erreur MySQL : {err}")

def update_notification_status(alarm_date):
    """Marque une alarme comme notifiée."""
    try:
        with mysql.connector.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE alarm_log SET notify = 1 WHERE alarm_date = %s;",
                    (alarm_date,)
                )
                conn.commit()
                print(f"Notification marquée comme envoyée pour l'alarme du {alarm_date}.")
    except mysql.connector.Error as err:
        print(f"Erreur MySQL lors de la mise à jour : {err}")

