<header class="navbar navbar-inverse navbar-fixed-top bs-docs-nav" role="banner">
    <div class="container">
        <div class="navbar-header">
            <button class="navbar-toggle" type="button" data-toggle="collapse" data-target=".bs-navbar-collapse">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
            <a href="index.php" class="navbar-brand">PiCar</a>
        </div>
        <nav class="collapse navbar-collapse bs-navbar-collapse" role="navigation">
            <ul class="nav navbar-nav">
                <li><a href="wifi.php">WiFi positioning</a></li>
                <li><a href="help.php">Help</a></li>
            </ul>
            <form class="navbar-form navbar-right" action="" method="post">
            <div class="form-group">
                <input type="text" id="data" placeholder="IP" class="form-control" value="192.168.0.220">
            </div>
            <button type="button" id="clickMe" class="btn btn-default" value="Connect" onclick="setupWebSocketConnection()">Connect</button>
        </form>
        </nav>
    </div>
</header>