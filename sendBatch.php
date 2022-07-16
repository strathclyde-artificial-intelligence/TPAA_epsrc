<?php

$code1 = $_GET["code1"];
$code2 = $_GET["code2"];
$code3 = $_GET["code3"];
$code4 = $_GET["code4"];


$curl = curl_init();

curl_setopt_array($curl, [
	CURLOPT_URL => "http://130.159.185.67:2358/submissions/batch?base64_encoded=true&wait=true&fields=*",
	CURLOPT_RETURNTRANSFER => true,
	CURLOPT_FOLLOWLOCATION => true,
	CURLOPT_ENCODING => "",
	CURLOPT_MAXREDIRS => 10,
	CURLOPT_TIMEOUT => 30,
	CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
	CURLOPT_CUSTOMREQUEST => "POST",
	CURLOPT_POSTFIELDS => "{
    \"submissions\": [
        {
            \"language_id\": 71,
            \"source_code\": \"$code1\"
        },
        {
            \"language_id\": 71,
            \"source_code\": \"$code2\"
        },
        {
            \"language_id\": 71,
            \"source_code\": \"$code3\"
        },
        {
            \"language_id\": 71,
            \"source_code\": \"$code4\"
        }
    ]
}",
	CURLOPT_HTTPHEADER => [
		"Content-Type: application/json",
	],
]);

$response = curl_exec($curl);
$err = curl_error($curl);

curl_close($curl);

if ($err) {
	echo "cURL Error #:" . $err;
} else {
	echo $response;
}
