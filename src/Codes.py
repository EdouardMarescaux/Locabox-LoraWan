from fastapi import FastAPI, HTTPException
import random
import mysql.connector
from Config import *

app = FastAPI()

def generate_code():
    """Génère un code à 6 chiffres."""
    return random.randint(100000, 999999)

def code_exists(code):
    """Vérifie si un code existe déjà dans la base."""
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM code_log WHERE code = %s", (code,))
    result = cursor.fetchone()[0]
    conn.close()
    return result > 0

def insert_unique_code(id_box):
    """Insère un code unique pour un id_box."""
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

@app.post("/generate-code/{id_box}")
def generate_and_insert_code(id_box: int):
    """
    API pour générer un code unique et l'insérer en base pour un id_box donné.
    """
    try:
        code = insert_unique_code(id_box)
        return {
            "id_box": id_box,
            "code_decimal": code,
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except mysql.connector.Error as db_err:
        raise HTTPException(status_code=500, detail=f"Erreur base de données: {db_err}")

