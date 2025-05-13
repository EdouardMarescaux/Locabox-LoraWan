from src.Codes import *
from src.Notification import * 
from src.ESP32 import *
from src.Acces import *
from src.Config import *
from src.Alarm import *
from src.Listener import *
from src.Message import *
from src.test import *
import time


def main():
    print("\nDémarrage des tests de l'application...\n")
    while True:
        #sendCode()
        #time.sleep(120)  # Envoie le code toutes les 2 minutes

    # Boucle principale du programme de test
    
        print("\n--- Menu de test ---")
        print("1. Envoyer un code manuellement")
        print("2. Simuler un accès (ouvrir le box)")
        print("3. Tester une notification")
        print("4. Reorganiser une trame manuellement")
        print("5. Quitter")
        print("6. Écouter les messages ChirpStack")
        print("---------------------")
        choix = input("Choix : ")

        if choix == '1':
            sendCode()
        elif choix == '2':
            handle_access(1)  # À remplacer par un ID dynamique
        elif choix == '3':
            SendNotificationToMobile(23, 'access')
        elif choix == '4':
            message = input("Entrer une trame : ")
            result = reorganize_trame(message)
            print("Message réorganisé :", result)
            parse_and_handle(result)
        elif choix == '5':
            print("Fermeture du programme.")
        elif choix == '6':
            listen_and_process()

if __name__ == "__main__":
    main()