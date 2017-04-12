<!DOCTYPE html>
<html>
<head>
	<title>PHP Unserializer</title>
	<meta charset="utf-8" />
</head>
<body style="font-family:monospace;">
<form method="post">
	PHP Serialized Data:<textarea name="string"></textarea>
	<input type="submit" value="submit" />
</form>
<br />
<pre>
<?php
    if (isset($_POST['string'])) {
        print_r(unserialize($_POST['string']));
    }
?>
</pre>
</body>
</html>
