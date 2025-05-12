import mysql.connector
from datetime import datetime
from src.Notification import *
from src.Config import *

def alarm_intrusion():
    """Surveille la base de données pour détecter une intrusion et envoyer une notification."""

    try:
        with mysql.connector.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                # Rechercher une intrusion non notifiée
                cursor.execute("""
                    SELECT alarm_log.alarm_date, alarm_log.id_box, id_user_box, LOWER(info) 
                    FROM alarm_log 
                    JOIN rent ON rent.id_box = alarm_log.id_box 
                    WHERE alarm_log.notify = 1 AND info = 'intrusion' 
                    LIMIT 1;
                """)
                result = cursor.fetchone()

                if not result:
                    # Aucun événement => on insère une alarme factice pour test
                    id_box = 1
                    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    cursor.execute("""
                        INSERT INTO alarm_log (alarm_date, id_box, info, notify)
                        VALUES (%s, %s, 'intrusion', 0)
                    """, (now, id_box))
                    conn.commit()
                    print(f"Aucune alarme non notifiée. Intrusion insérée pour le box {id_box}.")
                    return

                alarm_date, id_box, id_user, info = result

                print(f"Intrusion détectée sur le box {id_box}. Envoi de notification...")

                if info in messages:
                    if SendNotificationToMobile(id_user, info):
                        update_notification_status(alarm_date)
                else:
                    print(f"L'événement '{info}' n'existe pas dans le dictionnaire des messages.")

    except mysql.connector.Error as err:
        print(f"Erreur MySQL : {err}")

def update_notification_status(alarm_date):
    """Met à jour la base pour indiquer que la notification a été envoyée."""
    try:
        with mysql.connector.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE alarm_log SET notify = 1 WHERE alarm_date = %s;",
                    (alarm_date,)
                )
                conn.commit()
                print(f"Alarme du {alarm_date} marquée comme notifiée.")
    except mysql.connector.Error as err:
        print(f"Erreur MySQL lors de la mise à jour : {err}")
