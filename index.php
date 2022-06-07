<?php

$functionName = $_GET["func"];

if (function_exists($functionName)) { // check if function exists

	//The command below allows us to execture python scripts if necessary.
	//echo shell_exec("/usr/local/bin/python3 test.py");
    $functionName(); // run function
}


function One() {
	$problemOne = array("id"=>1, "statement"=>"given two numbers x and y multiply these number and return the result", "code"=>"def problemOne(x, y):", "solution"=>"def problemOne(x, y):\n\treturn x * y");

	echo json_encode($problemOne);
}

function Two() {
	$problemTwo= array("id"=>2, "statement"=>" given two numbers x and y add these numbers and print the output", "code"=>"def problemTwo(x, y):
", "solution"=>"def problemTwo(x, y):\n\tprint(x + y)");
	echo json_encode($problemTwo);
}

function Three() {
	$problemThree= array("id"=>3, "statement"=>"given a string s print each character of the string
", "code"=>"def problemTree(str):", "solution"=>"def problemTree(str):\n\tfor char in str:\n\t\tprint(char)");
	echo json_encode($problemThree);
}

function Four() {
	$problemFour= array("id"=>4, "statement"=>"check if the list contains the number that is passed through the parameters and return True if it contains the number and False otherwise
", "code"=>"def problemFour(list, number):", "solution"=>"def problemFour(list, number):\n\tfor num in list:\n\t\tif num == number:\n\t\t\treturn True\n\treturn False");
	echo json_encode($problemFour);
}

function Five() {
	$problemFive= array("id"=>5, "statement"=>"given a list of numbers print out all the numbers that are divisible by 5
", "code"=>"def problemFive(list):", "solution"=>"def problemFive(list):\n\tfor num in list:\n\t\tif num % 5 == 0:\n\t\t\tprint(num)");
	echo json_encode($problemFive);
}

?>
