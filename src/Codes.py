import random
import mysql.connector
from src.Config import *
from datetime import datetime

# Fonction pour générer un code à 6 chiffres
def generate_code():
    return random.randint(100000, 999999)

# Fonction pour vérifier si le code existe déjà dans la base de données
def code_exists(code):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM code_log WHERE code = %s", (code,))
    result = cursor.fetchone()[0]
    conn.close()
    return result > 0

# Fonction pour insérer un code unique dans la base de données avec un id_box valide
def insert_unique_code(id_box):
    if not id_box:
        raise ValueError("id_box ne peut pas être NULL ou vide")
    
    while True:
        code = generate_code()
        if not code_exists(code):
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO code_log (code, id_box) VALUES (%s, %s)", (code, id_box))
            conn.commit()
            conn.close()
            return code

# Fonction pour vérifier si un code valide a été utilisé avant l'ouverture
def is_valid_code_used(id_box):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Vérifier si un code existe pour cette box dans code_log
    cursor.execute("SELECT COUNT(*) FROM code_log WHERE id_box = %s", (id_box,))
    result = cursor.fetchone()[0]
    
    conn.close()
    return result > 0  # Retourne True si un code a été utilisé

# Fonction pour enregistrer une intrusion avec un id_box valide
def log_intrusion(id_box, info="Intrusion"):
    if not id_box:
        raise ValueError("id_box ne peut pas être NULL ou vide")

    # Vérifier si un code a été utilisé pour ouvrir la box
    if is_valid_code_used(id_box):
        print(f"✅ Aucun enregistrement d'intrusion, un code a été utilisé pour ouvrir la box {id_box}.")
        return

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Insérer l'intrusion avec la date et l'heure actuelles
    timestamp = datetime.now()
    cursor.execute("INSERT INTO alarm_log (alarm_date, info, id_box) VALUES (%s, %s, %s)", (timestamp, info, id_box))
    
    conn.commit()
    conn.close()

# ✅ Fonction pour insérer un DEVEUI dans la table box et mettre à jour modem
def insert_deveui(id_box, deveui):
    if not id_box or not deveui:
        raise ValueError("id_box et deveui ne peuvent pas être NULL ou vides")

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Vérifier si le DEVEUI existe déjà dans une autre box
    cursor.execute("SELECT id_box FROM box WHERE modem = %s", (deveui,))
    existing_box = cursor.fetchone()

    if existing_box and existing_box[0] != id_box:
        conn.close()
        raise ValueError(f"⚠️ ERREUR: Le DEVEUI {deveui} est déjà utilisé par le box {existing_box[0]} !")

    # Vérifier si l'id_box existe dans la table box
    cursor.execute("SELECT COUNT(*) FROM box WHERE id_box = %s", (id_box,))
    current_deveui = cursor.fetchone()[0]
    
    if current_deveui == deveui:
        # Le même DEVEUI est déjà enregistré pour ce box, donc on ne fait rien
        conn.close()
        print(f"✅ Aucun changement : Le DEVEUI {deveui} est déjà associé à la box {id_box}.")
        return

    if current_deveui:
        # Mettre à jour le DEVEUI du box
        cursor.execute("UPDATE box SET modem = %s WHERE id_box = %s", (deveui, id_box))
        print(f"🔄 Mise à jour : DEVEUI {deveui} mis à jour pour id_box {id_box}.")
    else:
        # Insérer une nouvelle ligne si l'id_box n'existe pas encore
        cursor.execute("INSERT INTO box (id_box, modem) VALUES (%s, %s)", (id_box, deveui))
        print(f"✅ Inséré : DEVEUI {deveui} ajouté pour id_box {id_box}.")

    conn.commit()
    conn.close()
