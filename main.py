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
        sendCode()
        time.sleep(120)  # Envoie le code toutes les 2 minutes

    # message = "MOKC AITE BOUS"
    # result = reorganize_trame(message)
    #print("Message traité :", result)
    #parse_and_handle(result)
    #SendNotificationToMobile(23, 'access')
    # Lancer l'écoute des messages de l'ESP32
    #listen_for_messages()
    #alarm_intrusion()

if __name__ == "__main__":
    main()