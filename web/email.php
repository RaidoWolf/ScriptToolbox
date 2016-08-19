<!DOCTYPE html>
<html>
<head>
<?php /*

    !!! WARNING !!!
    DO NOT JUST LEAVE THIS FILE ON YOUR SERVER IN A PUBLIC LOCATION! This file is
    deliberately vulnerable for the purpose of such things as SPF record checking,
    and as such, if you leave this file publicly accessible, anybody at all will be
    able to send an unlimited number of spoofed emails from your website. This is
    very bad. Don't be an idiot, please. Also, I take no responsibility for any kind
    of damage anybody may cause with this script.

*/ ?>
    <title>Multipart Email Tester</title>
    <meta charset="utf-8" />
    <style>
        textarea {
            height: 250px;
            width: 380px;
        }
        #header {
            margin: 0;
            padding: 0;
            display: block;
            width:100%;
            height: auto;
            background: #a0c0ff;
        }
    </style>
</head>
<body>
<div id="header">
    <form method="post">
        <label id="label-html" for="html">HTML</label>
        <textarea id="html" name="html"><?php echo htmlspecialchars($_POST['html']); ?></textarea>
        <label id="label-text" for="text">Text</label>
        <textarea id="text" name="text"><?php echo htmlspecialchars($_POST['text']); ?></textarea>
        <br />
        <label id="label-subject" for="subject">Subject</label>
        <input id="subject" name="subject" type="text" value="<?php echo htmlspecialchars($_POST['subject']); ?>" />
        <br />
        <label id="label-emailTo" for="emailTo">Email To</label>
        <input id="emailTo" name="emailTo" type="text" value="<?php echo htmlspecialchars($_POST['emailTo']); ?>" />
        <br />
        <label id="label-emailFromAddr" for="emailFromAddr">Email From Address</label>
        <input id="emailFromAddr" name="emailFromAddr" type="text" value="<?php echo htmlspecialchars($_POST['emailFromAddr']); ?>" />
        <br />
        <label id="label-emailFromName" for="emailFromName">Email From Name</label>
        <input id="emailFromName" name="emailFromName" type="text" value="<?php echo htmlspecialchars($_POST['emailFromName']); ?>" />
        <br />
        <label id="label-emailReplyAddr" for="emailReplyAddr">Email Reply-To Address</label>
        <input id="emailReplyAddr" name="emailReplyAddr" type="text" value="<?php echo htmlspecialchars($_POST['emailReplyAddr']); ?>" />
        <br />
        <label id="label-emailReplyName" for="emailReplyName">Email Reply-To Name</label>
        <input id="emailReplyName" name="emailReplyName" type="text" value="<?php echo htmlspecialchars($_POST['emailReplyName']); ?>" />
        <br />
        <input type="submit" name="submit" value="submit" />
    </form>
</div>
<?php
    if ($_POST['submit']) {
        $boundary = uniqid('JQQGQKQYQZWQWZ');

        $message =
            'This is a multi-part message in MIME format.'."\r\n"
        .   "\r\n"
        .   '--'.$boundary."\r\n"
        .   'Content-Transfer-Encoding: 7bit'."\r\n"
        .   'Content-Type: text/plain'."\r\n"
        .   "\r\n"
        .   (isset($_POST['text']) ? $_POST['text'] : '')."\r\n"
        .   '--'.$boundary."\r\n"
        .   'Content-Transfer-Encoding: 7bit'."\r\n"
        .   'Content-type: text/html'."\r\n"
        .   "\r\n"
        .   (isset($_POST['html']) ? $_POST['html'] : '')."\r\n"
        .   '--'.$boundary.'--'."\r\n";

        $headers =
            "MIME-Version: 1.0\r\n"
        .   "Content-type: multipart/alternative; boundary={$boundary}; charset=utf-8\r\n"
        .   "From: {$_POST['emailFromName']} <{$_POST['emailFromAddr']}>\r\n"
        .   "Reply-To: {$_POST['emailReplyName']} <{$_POST['emailReplyAddr']}>\r\n";
?>
<pre>
<?php
        $messageEscaped = htmlspecialchars($message);
        $headersEscaped = htmlspecialchars($headers);

        echo "Message source:\r\n\r\n{$messageEscaped}\r\n\r\n";
        echo "Message headers:\r\n\r\n{$headersEscaped}\r\n\r\n";
?>
</pre>
<?php
        mail(
            $_POST['emailTo'],
            $_POST['subject'],
            $message,
            $headers
        );
    }
?>
</body>
</html>
