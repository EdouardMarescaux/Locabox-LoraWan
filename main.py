from src.Codes import *
from src.Notification import * 
from src.ESP32 import *
from src.Acces import *
from src.Config import *



def main():
    print("Démarrage de l'application...")
    #sendCode()

    #generate_code()
    # Vérifier si la connexion fonctionne
    conn = mysql.connector.connect(**DB_CONFIG)
    if conn.is_connected():
        print("✅ Connexion à la base de données réussie !")
    else:
        print("❌ Échec de la connexion à la base de données.")
    conn.close()

    # Générer et insérer un code
    print("🔄 Génération d'un code unique...")
    code = insert_unique_code(1)

    # Vérifier si le code existe dans la base de données
    if code_exists(code):
        print(f"✅ Le code {code} existe déjà dans la base de données.")
    else:
        print(f"❌ Le code {code} n'existe pas.")

    print("🚀 Test d'envoi de notification...")
    
    # Envoie une notification pour une ouverture de box
    SendNotificationToMobile(23, "box ouvert")

    # Envoie une notification pour une intrusion
    SendNotificationToMobile(23, "intrusion")

if __name__ == "__main__":
    main()