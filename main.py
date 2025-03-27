from src.Codes import *
from src.Notification import * 
from src.ESP32 import *


def main():
    print("Démarrage de l'application...")
    # ESP32SendCode()
    sendCode()
    # SendNotificationToMobile(23, "Ratio dans tes morts", "Ratio dans tes grands morts User de con cordialement")

if __name__ == "__main__":
    main()