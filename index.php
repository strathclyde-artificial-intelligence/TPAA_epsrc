<?php

	$output = (exec("/usr/bin/python3 generator.py"));

	while($output == "False") {
		$output = (exec("/usr/bin/python3 generator.py"));
	}

	echo $output;
?>
