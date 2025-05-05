import mysql.connector
import requests
from src.Config import *
from src.Notification import *

def handle_access_message(id_box: int):
    """
    Gère un message d'accès reçu de l'ESP32.
    - Met à jour la base de données pour indiquer que le box est ouvert (locked = 0).
    - Envoie une notification à l'utilisateur.
    - Met à jour la variable notify à 1 dans la base de données.
    """
    if not id_box:
        raise ValueError("id_box ne peut pas être NULL ou vide")

    try:
        with mysql.connector.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                # Vérifier l'état actuel de 'locked' avant de le modifier
                cursor.execute("SELECT locked FROM access_log WHERE id_box = %s", (id_box,))
                current_status = cursor.fetchone()

                if current_status is None:
                    print(f"Aucun box trouvé avec l'id {id_box}.")
                    return

                if current_status[0] == 0:
                    print(f"Le box {id_box} est déjà ouvert.")
                    return  # Le box est déjà ouvert, donc pas besoin de le modifier

                # Étape 1 : Mettre à jour la colonne 'locked' à 0 (ouvrir le box)
                cursor.execute("UPDATE access_log SET locked = 0 WHERE id_box = %s", (id_box,))
                conn.commit()
                print(f"Le box {id_box} est maintenant ouvert (locked = 0).")

                # Étape 2 : Envoyer une notification
                SendNotificationToMobile(f"Accès autorisé au box {id_box}.")

                # Étape 3 : Mettre à jour la colonne 'notify' à 1
                cursor.execute("UPDATE box SET notify = 1 WHERE id_box = %s", (id_box,))
                conn.commit()
                print(f"Variable notify mise à jour pour le box {id_box} (notify = 1).")

    except mysql.connector.Error as err:
        print(f"Erreur lors de la mise à jour de la base de données : {err}")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'envoi de la notification : {e}")
