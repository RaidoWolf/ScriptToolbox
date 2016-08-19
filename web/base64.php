<!DOCTYPE html>
<html>
<head>
	<title>Base64 Tool</title>
	<meta charset="utf-8" />
</head>
<body style="font-family:monospace;">
<form>
	<select name="type" method="post">
		<option name="type" value="0">--SELECT TYPE--</option>
		<option name="type" value="enc">Encode</option>
		<option name="type" value="dec">Decode</option>
	</select>
	Input:<textarea name="string"></textarea>
	<input type="submit" value="submit" />
</form>
<br />
<?php
	if(isset($_REQUEST['type'])&&isset($_REQUEST['string']))
	{
		if(isset($_POST['type']))
		{
			$type = $_POST['type'];
		}
		elseif(isset($_GET['type']))
		{
			$type = $_GET['type'];
		}
		else
		{
			echo "<p>Please select a type!</p>";
		}
		if(isset($_POST['string']))
		{
			$string = $_POST['string'];
		}
		elseif(isset($_GET['string']))
		{
			$string = $_GET['string'];
		}
		else
		{
			echo "<p>Please enter input!</p>";
		}
		if(isset($type)&&isset($string))
		{
			if($type == enc)
			{
				$base64 = base64_encode($string);
				if(strlen($base64)<32)
				{
					echo $base64;
				}
				else
				{
					$startStringPos = 0;
					for($i=0; (($i+1)*32)<strlen($base64); $i++)
					{
					$substrOutput = substr($base64,$startStringPos,32);
					echo $substrOutput."\n";
					$startStringPos = $startStringPos + 32;
					}
				}
			}
			elseif($type == dec)
			{
				$ascii = base64_decode($string);
				echo $ascii;
			}
			else {}
		}
		else {}
	}
	else
	{
		echo "<p>Please select a type and enter input</p>";
	}
?>
</body>
</html>
