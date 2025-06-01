<?php
// src/send_notification.php


define("NOTIFICATION_URL", "http://172.16.0.30:3000/send-notification");

$messages = [
    'intrusion' => "Une intrusion a été détectée dans votre box.",
    'ouverture' => "Votre box a été ouverte avec succès.",
    'code_errone' => "Un code incorrect a été saisi."
];

$titles = [
    'intrusion' => "Alerte Sécurité",
    'ouverture' => "Accès Autorisé",
    'code_errone' => "Erreur d'Authentification"
];

function sendNotificationToMobile($userId, $event)
{
    global $messages, $titles;

    $event = strtolower($event);

    if (!isset($messages[$event]) || !isset($titles[$event])) {
        echo "Erreur : L'événement '$event' n'existe pas dans la configuration.\n";
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

    if ($result === FALSE) {
        echo "Erreur réseau lors de l'envoi de la notification.\n";
        return false;
    }

    // Facultatif : décoder la réponse si tu veux un retour plus précis
    $httpCode = $http_response_header[0] ?? '';
    if (strpos($httpCode, "200") !== false) {
        echo "Notification envoyée avec succès à l'utilisateur $userId.\n";
        return true;
    } else {
        echo "Erreur lors de l'envoi : réponse = $httpCode\n";
        return false;
    }
}

sendNotificationToMobile(23, 'intrusion');

