import mysql.connector
import requests
from src.Config import *
from src.Notification import *

def handle_access(id_box: int):
    if not id_box:
        raise ValueError("id_box ne peut pas être NULL ou vide")

    try:
        with mysql.connector.connect(**DB_CONFIG) as conn:
            with conn.cursor(buffered=True) as cursor:
                # Vérifie l'état actuel du box
                cursor.execute("SELECT locked FROM access_log WHERE id_box = %s", (id_box,))
                current_status = cursor.fetchone()

                if current_status is None:
                    print(f"Aucun box trouvé avec l'id {id_box}.")
                    return

                if current_status[0] == 0:
                    print(f"Le box {id_box} est déjà ouvert.")
                    return

                # Mettre locked = 0 (ouvrir le box)
                cursor.execute("UPDATE access_log SET locked = 0 WHERE id_box = %s", (id_box,))
                conn.commit()

                # Insertion dans access_log (journalisation de l'accès)
                cursor.execute("""
                    INSERT INTO access_log (id_box, event_type, event_time)
                    VALUES (%s, %s, NOW())
                """, (id_box, 'access'))
                conn.commit()
                print(f"Événement d'accès inséré pour le box {id_box}.")

                # Envoyer la notification
                user_id = 23  # À remplacer dynamiquement si possible
                SendNotificationToMobile(user_id, 'access')

                # Marquer la notification comme envoyée
                cursor.execute("UPDATE access_log SET notify = 1 WHERE id_box = %s", (id_box,))
                conn.commit()

                print(f"Le box {id_box} est maintenant ouvert et notifié.")

    except mysql.connector.Error as err:
        print(f"Erreur MySQL : {err}")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'envoi de la notification : {e}")
