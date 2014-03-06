<!DOCTYPE html>
<html>
    <head>
		<?php require_once("headermeta.php") ;?>
        <script type="text/javascript" src="functions.js"></script>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title></title>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    </head>
    <?php
        $myFile = "file.txt";
        $fh = fopen($myFile, 'r');
        $theData = fread($fh, filesize($myFile));
        fclose($fh);
        list($portal, $airmon, $l319, $l320) = split(',', $theData);
        ?>
        <body onload="timedRefresh(5000); drawCircle(<?php echo $portal ?>, <?php echo $airmon; ?>,<?php echo $l319; ?>,<?php echo $l320; ?>);">
		<?php require_once("navbar.php"); ?>
        <canvas style="width: 1600px; height: 800px; background-image: url('bg2.jpg'); background-repeat: no-repeat; background-size: 1500px 700px" id="surface" width="1440" height="546"> . </canvas>
        </body>
</html>

