<!DOCTYPE html>
<html>
<head>
<title>Convert RGB to Hexadecimal</title>
<meta charset="utf-8" />
</head>
<body>
	<form method="post">
		R:<input type="text" name="r" id="r" value=<?php echo '"'.$_POST['r'].'"'; ?> />
		G:<input type="text" name="g" id="g" value=<?php echo '"'.$_POST['g'].'"'; ?> />
		B:<input type="text" name="b" id="b" value=<?php echo '"'.$_POST['b'].'"'; ?> />
		<input type="submit" value="submit" />
	</form>
	<?php
		if(isset($_POST['r']))
		{
			$r = $_POST['r'];
		}
		elseif(isset($_GET['r']))
		{
			$r = $_GET['r'];
		}
		if(isset($_POST['g']))
		{
			$g = $_POST['g'];
		}
		elseif(isset($_GET['g']))
		{
			$g = $_GET['g'];
		}
		if(isset($_POST['b']))
		{
			$b = $_POST['b'];
		}
		elseif(isset($_GET['b']))
		{
			$b = $_GET['b'];
		}
		if((0<=$r)&&($r<=255)&&(0<=$g)&&($g<=255)&&(0<=$b)&&($b<=255))
		{
		$r = sprintf('%1$02s', dechex($r));
		$g = sprintf('%1$02s', dechex($g));
		$b = sprintf('%1$02s', dechex($b));
		$output = strtoupper($r.$g.$b);
		echo "<p style='font-family:monospace;font-size:16pt;'>0x",$output,"</p>";
		}
		else
		{
		echo "<p style='font-family:monospace;font-size:16pt;'>Invalid Input!</p>";
		}
	?>
</body>
</html>
