import mysql.connector

# Configuration de la base de données
DB_CONFIG = {
    "host": "ext.epid-vauban.fr",
    "user": "locabox",
    "password": "locabox2025!",
    "database": "locabox"
}

def is_box_open(id_box: int) -> int:
    """
    Vérifie si une box est ouverte dans la base de données.
    Retourne 1 si la box est ouverte, sinon 0.
    """

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        # Exemple d'une table 'box' avec un champ 'status' qui représente l'état de la box
        cursor.execute("SELECT locked FROM access_log WHERE id_box = %s", (id_box,))
        result = cursor.fetchone()
        
        if result is not None:
            # Si status == 1, la box est ouverte, sinon elle est fermée
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

# Test de la fonction
if __name__ == "__main__":
    id_box = 1  # Remplace par l'ID réel de la box à tester
    status = is_box_open(id_box)
    print(f"État du box {id_box}: {'Fermé' if status == 1 else 'Ouvert'}")
