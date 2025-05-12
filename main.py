from Codes import *
from Notification import * 
from ESP32 import *
from Acces import *
from Config import *
from Alarm import *
from Listener import *


def main():
    print("\nDémarrage des tests de l'application...\n")
    sendCode()
    #SendNotificationToMobile(23, 'intrusion')
    # Lancer l'écoute des messages de l'ESP32
    #listen_for_messages()
    #alarm_intrusion()

if __name__ == "__main__":
    main()