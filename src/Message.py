from Alarm import *
#import src.Codes as codes
from Acces import *
from Config import *

# Dictionnaire qui décrit les clés et combien de paramètres elles attendent (en longueur de caractères)
key_parameters = {
    "M": [2],
    "C": [2],
    "A": [2],
    "E": [2],
    "B": [2],
    "S": [],
}

# Fonctions pour chaque paramètre
def handle_DR(): print("Handle DR: Démarrage")
def handle_OK(): print("Handle OK: Accès autorisé")
def handle_NC(): print("Handle NC: Nouveau code")
def handle_CR(): print("Handle RC: Code reçu")
def handle_DC(): print("Handle DC: Demande code")
def handle_EC(): print("Handle EC: Erreur code")
def handle_IT(): alarm_intrusion()
def handle_DV(): print("Handle DV: Déverrouiller")
def handle_VR(): print("Handle VR: Verrouiller")
def handle_CF(): print("Handle CF: Code faux")
def handle_OU(): handle_access_message(1)  # Exemple d'ID de box
def handle_FE(): print("Handle BF: Box fermé")

# Association paramètres → fonctions
param_handlers = {
    "DR": handle_DR,
    "OK": handle_OK,
    "NC": handle_NC,
    "CR": handle_CR,
    "DC": handle_DC,
    "EC": handle_EC,
    "IT": handle_IT,
    "DV": handle_DV,
    "VR": handle_VR,
    "CF": handle_CF,
    "OU": handle_OU,
    "FE": handle_FE,
}


def reorganize_trame(message: str):
    result = []  # Liste pour stocker les caractères et espaces traités

    for char in message:
        result.append(char)  # Ajouter chaque caractère
        if char == " ":  # Si l'on rencontre un espace
            result.append(" ")  # Ajouter un espace supplémentaire juste après

    return ''.join(result) 

# Test de la fonction
message = "MOKC AITE BOUS"
result = reorganize_trame(message)
print(result)  # Affiche le message avec les espaces traités



def parse_and_handle(message: str):
    if not message.endswith("S"):
        raise ValueError("Le message doit se terminer par 'S'")
    else:
        if message[1:3] in param_handlers.keys():
            print(message[1:3])
            param_handlers[message[1:3]]()
        if message[4:6] in param_handlers.keys():
            print(message[4:6])
            param_handlers[message[4:6]]()
        if message[7:9] in param_handlers.keys():
            print(message[7:9])
            param_handlers[message[7:9]]()
        if message[10:12] in param_handlers.keys():
            print(message[10:12])
            param_handlers[message[10:12]]()     
        if message[13:15] in param_handlers.keys():
            print(message[13:15])
            param_handlers[message[13:15]]()
            
    
parse_and_handle(result)