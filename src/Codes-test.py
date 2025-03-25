import random
import mysql.connector
from datetime import datetime

# Fonction pour générer un code à 6 chiffres
def generate_code():
    return random.randint(100000, 999999)

# Fonction pour vérifier si le code existe déjà dans la base de données
def code_exists(code):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="test"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM codes WHERE valeur = %s", (code,))
    result = cursor.fetchone()[0]
    conn.close()
    return result > 0

# Fonction pour insérer un code unique dans la base de données
def insert_unique_code():
    while True:
        code = generate_code()
        if not code_exists(code):
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="test"
            )
            cursor = conn.cursor()
            cursor.execute("INSERT INTO codes (valeur) VALUES (%s)", (code,))
            conn.commit()
            conn.close()
            return code
        
def log_intrusion(event="Intrusion détectée"):
    # Connexion à la base de données MySQL
    conn = mysql.connector.connect(
        host="localhost",        # Adresse de ton serveur MySQL
        user="root",             # Ton utilisateur MySQL
        password="",             # Ton mot de passe MySQL
        database="test"          # Nom de la base de données
    )
    
    cursor = conn.cursor()
    
    # Insérer l'intrusion avec la date et l'heure actuelles
    timestamp = datetime.now()
    cursor.execute("INSERT INTO intrusions (event, created_at) VALUES (%s, %s)", (event, timestamp))
    
    # Valider et fermer la connexion
    conn.commit()
    conn.close()

# # Exemple d'appel pour enregistrer une intrusion
# log_intrusion("Intrusion dans la zone sécurisée")

# # Générer et insérer un code unique
# code = insert_unique_code()
# print(f"Generated Unique Code: {code}")

