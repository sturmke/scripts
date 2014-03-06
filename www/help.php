<!DOCTYPE html>
<html lang="nl">

<head>
    <?php require_once("headermeta.php"); ?>
</head>

<body>
<?php require_once("navbar.php"); ?>

<div class="container">
    <div class="panel panel-primary">
        <!-- Default panel contents -->
        <div class="panel-heading"></div>

        <div class="panel-body">
            <h4>Keyboard</h4>
            <table class="table table-striped">
                <thead>
                <tr>
                    <th>Input</th>
                    <th>Response</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>Arrow up</td>
                    <td>Forward</td>
                </tr>
				<tr>
                    <td>Arrow left</td>
                    <td>Left</td>
                </tr>
				<tr>
                    <td>Arrow right</td>
                    <td>Right</td>
                </tr>
                <tr>
                    <td>Arrow down</td>
                    <td>Reverse</td>
                </tr>
				<tr>
                    <td>Space</td>
                    <td>Stop</td>
                </tr>
				<tr>
                    <td>Key A</td>
                    <td>Fast left</td>
                </tr>
				<tr>
                    <td>Key Z</td>
                    <td>Fast Right</td>
                </tr>
				
                </tbody>
            </table>

            <h4>PS3 controller</h4>
            <table class="table table-striped">
                <thead>
                <tr>
                    <th>Input</th>
                    <th>Response</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>R2</td>
                    <td>Forward</td>
                </tr>
				<tr>
                    <td>L1</td>
                    <td>Left</td>
                </tr>
				<tr>
                    <td>R1</td>
                    <td>Right</td>
                </tr>
                <tr>
                    <td>L2</td>
                    <td>Reverse</td>
                </tr>
				<tr>
                    <td>Cross</td>
                    <td>Stop</td>
                </tr>
				<tr>
                    <td>Arrow Left</td>
                    <td>Fast left</td>
                </tr>
				<tr>
                    <td>Arrow Right</td>
                    <td>Fast Right</td>
                </tr>
				</tbody>
            </table>
        </div>

    </div>
    <?php require_once("footer.php"); ?>
</div>

</body>

</html>