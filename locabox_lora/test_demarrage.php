<?php
$url = 'http://localhost/update.php'; // Remplace par l'URL réelle de ton webhook

// Trame "ADRCEEEE" = M:DR (Démarrage), C:CE, A:EE, E:EE, B: (optionnel)
// Codée en base64 :
$trameTexte = "ADRCEEEE";
$trameBase64 = base64_encode($trameTexte);

// devEUI de test (modem dans la table box) : fffe3884ab08b764
$devEuiHex = "fffe3884ab08b764";
$devEuiBase64 = base64_encode(hex2bin($devEuiHex));

// Payload simulé
$payload = json_encode([
    'devEUI' => $devEuiBase64,
    'data' => $trameBase64
]);

$options = [
    'http' => [
        'method'  => 'POST',
        'header'  => "Content-Type: application/json",
        'content' => $payload
    ]
];

$context = stream_context_create($options);
$response = file_get_contents($url, false, $context);

echo "Réponse du serveur :\n";
echo $response;
