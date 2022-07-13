<?php

	$output = (exec("/usr/bin/python3 generator.py"));

	//$difficulty = "3";
	while($output == "False") {
		$output = (exec("/usr/bin/python3 generator.py"));
	}

	echo $output;
?>
