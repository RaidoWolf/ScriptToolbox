<!DOCTYPE html>
<html>
<head>
<title>Translate to NATO Phoenetic Code</title>
<meta charset="utf-8" />
</head>
<body>
	<form method="post">
		Text:<input type="text" name="string" id="string" />
		<input type="submit" value="submit" />
	</form>
	<?php
		$string = $_REQUEST['string'];
		$string = strtolower($string);
		$dictionary = array(
				'a' => 'Alpha ',
				'b' => 'Bravo ',
				'c' => 'Charlie ',
				'd' => 'Delta ',
				'e' => 'Echo ',
				'f' => 'Foxtrot ',
				'g' => 'Golf ',
				'h' => 'Hotel ',
				'i' => 'India ',
				'j' => 'Juliet ',
				'k' => 'Kilo ',
				'l' => 'Lima ',
				'm' => 'Mike ',
				'n' => 'November ',
				'o' => 'Oscar ',
				'p' => 'Papa ',
				'q' => 'Quebec ',
				'r' => 'Romeo ',
				's' => 'Sierra ',
				't' => 'Tango ',
				'u' => 'Uniform ',
				'v' => 'Victor ',
				'w' => 'Whiskey ',
				'x' => 'X-Ray ',
				'y' => 'Yankee ',
				'z' => 'Zulu '
		);
		$output = strtr($string,$dictionary);
		echo "<p>",$output,"</p>";
	?>
</body>
</html>
