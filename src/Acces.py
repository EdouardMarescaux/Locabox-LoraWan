import mysql.connector
from src.Config import *

def is_box_open(id_box: int) -> int:
    """
    Vérifie si un box est ouvert dans la base de données.
    Retourne 1 si le box est ouvert, sinon 0.
    """

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        # Exemple d'une table 'box' avec un champ 'status' qui représente l'état du box
        cursor.execute("SELECT locked FROM access_log WHERE id_box = %s", (id_box,))
        result = cursor.fetchone()
        
        if result is not None:
            # Si status == 1, le box est ouvert, sinon il est fermé
            status = result[0]
            if status == 1:
                print(f"Le box {id_box} est fermé.")
                return 1
            else:
                print(f"Le box {id_box} est ouvert.")
                return 0
        else:
            print(f"Aucun box trouvé avec l'id {id_box}.")
            return 0
    
    except mysql.connector.Error as err:
        print(f"Erreur lors de la connexion à la base de données: {err}")
        return 0
    
    finally:
        conn.close()
