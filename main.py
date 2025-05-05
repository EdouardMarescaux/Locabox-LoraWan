from src.Codes import *
from src.Notification import * 
from src.ESP32 import *
from src.Acces import *
from src.Config import *
from src.Alarm import *
from src.Listener import *


def main():
    print("\nDémarrage des tests de l'application...\n")
    sendCode()
    #SendNotificationToMobile(23, 'intrusion')
    # Lancer l'écoute des messages de l'ESP32
    #listen_for_messages()
    #alarm_intrusion()

if __name__ == "__main__":
    main()