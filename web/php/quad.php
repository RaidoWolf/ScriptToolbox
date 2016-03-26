<html>
<head>
	<title>PHP Quadratic Solver</title>
	<meta charset="utf-8">
</head>
<body>
<?php
if (isset($_REQUEST['a'], $_REQUEST['b'], $_REQUEST['c']))
	{
	echo "<form method='post' action='quad.php'>
	A: <input name='a' type='text'>
	B: <input name='b' type='text'>
	C: <input name='c' type='text'><br>
	</textarea><br>
	<input type='submit'>
	</form>";
	$a = $_REQUEST['a'];
	$b = $_REQUEST['b'];
	$c = $_REQUEST['c'];
	echo "1:", (((-$b)+sqrt((pow($b,2))-(4*$a*$c)))/(2*$a)), "<br>";
	echo "2:", (((-$b)-sqrt((pow($b,2))-(4*$a*$c)))/(2*$a)), "<br>";
	}
else
	{
	echo "<form method='post' action='quad.php'>
	A: <input name='a' type='text'>
	B: <input name='b' type='text'>
	C: <input name='c' type='text'><br>
	</textarea><br>
	<input type='submit'>
	</form>";
	}
?>
<p>ax<sup>2</sup>+bx+c=0</p>
</body>
</html>