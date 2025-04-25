import mysql.connector
from src.Notification import *
from src.Config import *

def alarm_intrusion():
    """Surveille la base de données pour détecter une intrusion et envoyer une notification."""

    
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    notifier = False

    try:
        # Recherche d'une intrusion non encore notifiée
        cursor.execute("""
            SELECT alarm_log.alarm_date, alarm_log.id_box, id_user_box, LOWER(info) 
            FROM alarm_log 
            JOIN rent ON rent.id_box = alarm_log.id_box 
            WHERE alarm_log.notify = 0 AND info = 'intrusion' 
            LIMIT 1;
        """)
        result = cursor.fetchone()

        if result:
            # Si status == 1, le box est ouvert, sinon il est fermé
            alarm_date, id_box, id_user, info = result  # Extraction correcte
            
            if info.lower() in messages:
                notifier = SendNotificationToMobile(id_user, info.lower())
            else:
                print(f"Erreur : L'événement '{info}' n'existe pas dans messages.")

    except mysql.connector.Error as err:
        print(f"Erreur lors de la connexion à la base de données: {err}")
        return 0

    finally:
        conn.close()

    # Mise à jour si une notification a été envoyée
    if notifier:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("UPDATE alarm_log SET notify = 1 WHERE alarm_date = %s;", (alarm_date,))
        conn.commit()
        conn.close()
