from src.Codes import *
from src.Notification import * 
from src.ESP32 import *
from src.Acces import *
from src.Config import *



def main():
    print("\n🚀 Démarrage des tests de l'application...\n")

    while True:
        #trouver une intrusion
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        notifier=False
        
        try:
            # Exemple d'une table 'box' avec un champ 'status' qui représente l'état du box
            cursor.execute("SELECT alarm_log.alarm_date,alarm_log.id_box,id_user_box,info FROM alarm_log,rent WHERE rent.id_box = alarm_log.id_box and info="intrusion" LIMIT 1;")
            result = cursor.fetchone()
            
            if result is not None:
                # Si status == 1, le box est ouvert, sinon il est fermé
                status = result[0]
                notifier=SendNotificationToMobile(status[2],status[3])

                
        
        except mysql.connector.Error as err:
            print(f"Erreur lors de la connexion à la base de données: {err}")
            return 0
        
        finally:
            conn.close()
            pass

        if notifier==True:
             conn = mysql.connector.connect(**DB_CONFIG)
             cursor = conn.cursor()
             cursor.execute("UPDATE `alarm_log`  SET notifier =1 WHERE alarm_date="+status[0]+";")
             conn.close()
             
if __name__ == "__main__":
    main()