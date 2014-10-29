<!DOCTYPE html>
<html>
<head>
<title>Invert Hexadecimal Value</title>
<meta charset="utf-8" />
</head>
<body>
	<form method="post">
		Text:<input type="text" name="string" id="string" />
		<input type="submit" value="submit" />
	</form>
	<?php
		$string = $_REQUEST['string'];
		$string = strtoupper($string);
		$dictionary = array(
				'0' => 'F',
				'1' => 'E',
				'2' => 'D',
				'3' => 'C',
				'4' => 'B',
				'5' => 'A',
				'6' => '9',
				'7' => '8',
				'8' => '7',
				'9' => '6',
				'A' => '5',
				'B' => '4',
				'C' => '3',
				'D' => '2',
				'E' => '1',
				'F' => '0'
		);
		$output = strtr($string,$dictionary);
		echo "<p>",$output,"</p>";
	?>
</body>
</html>
