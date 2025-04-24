from src.Codes import *
from src.Notification import * 
from src.ESP32 import *
from src.Acces import *
from src.Config import *
from src.Alarm import *


def main():
    print("\nDémarrage des tests de l'application...\n")
    sendCode()
    #alarm_intrusion()

if __name__ == "__main__":
    main()