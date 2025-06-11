<?php

header("Content-type: application/json");
$fp=@fopen("TMP.txt","a");
fwrite($fp,"\r\n"."appel"."\r\n");

// Connexion à la base de données MySQL
$host = "ext.epid-vauban.fr";
$user = "locabox";
$password = "locabox2025!";
$dbname = "locabox";

$messages = [
    'intrusion' => "Une intrusion a été détectée dans votre box.",
    'ouverture' => "Votre box a été ouvert avec succès.",
	'fermeture' => "Votre box a été fermé avec succès.",
    'code_errone' => "Un code incorrect a été saisi."
];

$titles = [
    'intrusion' => "Alerte Sécurité",
    'ouverture' => "Box Ouvert",
];

define("NOTIFICATION_URL", "http://172.16.0.30:3000/send-notification");

// Fonction d'envoi de notification
function sendNotificationToMobile($userId, $event)
{
    global $messages, $titles;

    $event = strtolower($event);
    if (!isset($messages[$event]) || !isset($titles[$event])) {
        return false;
    }

    $payload = [
        'userId' => $userId,
        'title' => $titles[$event],
        'body' => $messages[$event]
    ];

    $options = [
        'http' => [
            'header'  => "Content-Type: application/json\r\n",
            'method'  => 'POST',
            'content' => json_encode($payload),
            'timeout' => 5
        ]
    ];

    $context = stream_context_create($options);
    $result = @file_get_contents(NOTIFICATION_URL, false, $context);

    $httpCode = $http_response_header[0] ?? '';
    return $result !== false && strpos($httpCode, "200") !== false;
}

$json=file_get_contents("php://input");
$obj=json_decode($json);
try {
	$bdd = new PDO("mysql:host=$host;dbname=$dbname", $user, $password);
	echo "mysql:host=$host;dbname=$dbname", $user, $password;
} 
catch (PDOException $e) {
	echo "Erreur : " . $e->getMessage();
    fwrite($fp, "Erreur connexion BDD : " . $e->getMessage() . "\r\n");
    fclose($fp);
    exit; // Arrête le script proprement si connexion échouée
}

try{
	
	$trame=base64_decode(json_encode($obj->data));
	$id=json_encode($obj->devEUI);
	$deveui=bin2hex(base64_decode($id));
	fwrite($fp,$trame."\r\n");
	fwrite($fp,$deveui."\r\n");
	$M=substr($trame,1,2);
	$C=substr($trame,4,2);
	$A=substr($trame,7,2);
	$E=substr($trame,10,2);
	$B=substr($trame,13,2);
	fwrite($fp,"M:".$M."\r\n");
	fwrite($fp,"C:".$C."\r\n");
	fwrite($fp,"A:".$A."\r\n");
	fwrite($fp,"E:".$E."\r\n");
	fwrite($fp,"B:".$B."\r\n");
	

	$query = $bdd->query("SELECT id_box FROM `box` WHERE modem='$deveui'");
	$id_box = $query->fetchall()[0][0];
	echo "id box = " .$id_box;
	$query->closeCursor();
	
	fwrite($fp,"id_box = ".$id_box."\r\n");
	
	// En vie
	if ($M== "OK"){
		$bdd->exec("UPDATE box SET state = NOW() WHERE id_box = $id_box");
	}
	
	// Démarrage
	if ($M == "DR") {
		// Générer un code aléatoire à 6 chiffres
		$code = str_pad(strval(random_int(100000, 999999)), STR_PAD_LEFT);
		fwrite($fp, "Code genere : $code\r\n");
		// Mettre à jour des colonnes de la table box
		$bdd->exec("UPDATE box SET current_code = '$code', state = NOW(), start_up = '1' WHERE id_box = $id_box");
		// Insérer dans la table code_log
		$bdd->exec("INSERT INTO code_log (code, id_box, sending_date, issued) VALUES ($code, $id_box, NOW(), '1')");
	
		// Appeler le script Python pour envoyer le code à l'ESP32
		$escaped_code = escapeshellarg($code);
		$escaped_dev = escapeshellarg($deveui);
		$script = escapeshellarg("/Locabox LoraWan/src/ESP32.py");
		$command = "python3 $script $escaped_dev $escaped_code";
		$output = shell_exec($command);
		fwrite($fp, "Script Python execute: $command\r\nRetour: $output\r\n");
	}
	
	// Réception du code
	if ($C== "CR"){
		$bdd->exec("UPDATE code_log SET received = 1 WHERE code = '$code' AND id_box = '$id_box' ORDER BY code_date DESC LIMIT 1");
	}

	// Intrusion
	if ($A== "IT"){
		$bdd->exec("INSERT INTO alarm_log (info, id_box, notify) VALUES ('Intrusion', $id_box, 0)");
        fwrite($fp,"intrusion inseree"."\r\n");
		
		// Envoi de la notification ouverture
		if (sendNotificationToMobile(23, 'intrusion')) {
			fwrite($fp, "Notification d'intrusion envoyée avec succès\r\n");
			$bdd->exec("UPDATE alarm_log SET notify = 1 WHERE id_box = $id_box ORDER BY alarm_date DESC LIMIT 1");
		} 
		else {
			fwrite($fp, "Échec de l'envoi de la notification d'intrusion\r\n");
		}
	}
	
	// Ouverture
	if ($B== "OU"){
        $bdd->exec("UPDATE access_log SET locked = '0', access_date = NOW(), notify = '0' WHERE id_box = $id_box");
		fwrite($fp,"box ouvert"."\r\n");
		
		// Envoi de la notification ouverture
		if (sendNotificationToMobile(23, 'ouverture')) {
			fwrite($fp, "Notification ouverture envoyée avec succès\r\n");
			$bdd->exec("UPDATE access_log SET notify = 1 WHERE id_box = $id_box ORDER BY access_date DESC LIMIT 1");
		} 
		else {
			fwrite($fp, "Échec de l'envoi de la notification ouverture\r\n");
		}
	}
	
	// Fermeture
	if ($B== "FE"){
        $bdd->exec("UPDATE access_log SET locked = '1', access_date = NOW(), notify = '0' WHERE id_box = $id_box");
		fwrite($fp,"box ferme"."\r\n");
	}
	
	fclose($fp);
}
catch (PDOException $e) {
	echo "Erreur : " . $e->getMessage();
}


?>