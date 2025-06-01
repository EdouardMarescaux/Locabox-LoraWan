# Configuration de la base de données
DB_CONFIG = {
    "host": "ext.epid-vauban.fr",
    "user": "locabox",
    "password": "locabox2025!",
    "database": "locabox"
}

# --- 🔗 Connexion au serveur Chirpstack ---
CHIRPSTACK_SERVER = "172.16.0.49:8080"

# DevEUI de l'ESP32
dev_eui = bytes([0xff, 0xfe, 0x38, 0x84, 0xab, 0x08, 0xb7, 0x64])

# Clé API pour l'authentification avec Chirpstack
API_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcGlfa2V5X2lkIjoiMjU1ZTFlMTktZjQ2Mi00MDBlLWIyYTUtYWYwNjJmMjgyYzQ1IiwiYXVkIjoiYXMiLCJpc3MiOiJhcyIsIm5iZiI6MTc0MTg3Mzk5MSwic3ViIjoiYXBpX2tleSJ9.iUvxw_hVlA9M5lG8oppcH97jlidi061wDJWSPRGzxCo"

# --- 📲 Configuration des notifications ---
NOTIFICATION_URL = "http://172.16.0.30:3000/send-notification"

# ID utilisateur pour l'envoi des notifications (modifiable dynamiquement)
user_id = 23

# Messages types pour les notifications
messages = {
    "intrusion": "Une intrusion a été détectée dans votre box !",
    "access": "Accès autorisé à votre box.",
}
titles = {
    "intrusion": "Alerte de votre box !",
    "access": "Information box",
}
