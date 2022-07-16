<?php

$token1 = $_GET["token1"];
$token2 = $_GET["token2"];
$token3 = $_GET["token3"];
$token4 = $_GET["token4"];

$curl = curl_init();

curl_setopt_array($curl, [
	CURLOPT_URL => "http://130.159.185.67:2358/submissions/batch?tokens=$token1,$token2,$token3,$token4&base64_encoded=true&wait=true&fields=*",
	CURLOPT_RETURNTRANSFER => true,
	CURLOPT_FOLLOWLOCATION => true,
	CURLOPT_ENCODING => "",
	CURLOPT_MAXREDIRS => 10,
	CURLOPT_TIMEOUT => 30,
	CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
	CURLOPT_CUSTOMREQUEST => "GET",
]);

$response = curl_exec($curl);
$err = curl_error($curl);

curl_close($curl);

if ($err) {
	echo "cURL Error #:" . $err;
} else {
	echo $response;
}
