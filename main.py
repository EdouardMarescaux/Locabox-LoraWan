from src.Codes import *
from src.Notification import * 
from src.ESP32 import *
from src.Acces import *


def main():
    print("Démarrage de l'application...")
    #sendCode()

    generate_code()
    code = insert_unique_code(1)
    # Vérifier si le code existe dans la base de données
    if code_exists(code):
        print(f"✅ Le code {code} existe déjà dans la base de données.")
    else:
        print(f"❌ Le code {code} n'existe pas.")
    #insert_deveui(1, bytes([0xff, 0xfe, 0x38, 0x84, 0xab, 0x08, 0xb7, 0x64]))    
    #is_valid_code_used(1)
    #log_intrusion(1, info="Intrusion")


    #is_box_open(1)
    # SendNotificationToMobile(23, "Ratio dans tes morts", "Ratio dans tes grands morts User de con cordialement")

if __name__ == "__main__":
    main()