<html>
<body>
<?php
if (isset($_REQUEST['domain']))
	{
	echo "<form method='post' action='dig.php'>
	Domain Name: <input name='domain' type='text'><br>
	</textarea><br>
	<input type='submit'>
	</form>";
	$domain = $_REQUEST['domain'];
	echo "<a href='?domain=$domain'>permalink</a><br>";
	$result = dns_get_record("$domain");
	print("<pre>".print_r($result,true)."</pre>");
	}
else
	{
	echo "<form method='post' action='dig.php'>
	Domain Name: <input name='domain' type='text'><br>
	</textarea><br>
	<input type='submit'>
	</form>";
	}
?>
</body>
</html>
