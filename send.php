<?php

	$codeUser = $_GET["code"];

	$curl = curl_init();

	curl_setopt_array($curl, [
	CURLOPT_URL => "http://130.159.185.67:2358/submissions?base64_encoded=true&wait=true&fields=*",
	CURLOPT_RETURNTRANSFER => true,
	CURLOPT_FOLLOWLOCATION => true,
	CURLOPT_ENCODING => "",
	CURLOPT_MAXREDIRS => 10,
	CURLOPT_TIMEOUT => 30,
	CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
	CURLOPT_CUSTOMREQUEST => "POST",
	CURLOPT_POSTFIELDS => "{
	\"language_id\": 71,
	\"source_code\": \"$codeUser\",
	\"stdin\": \"SnVkZ2Uw\"
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
?>


