<!DOCTYPE html> <html lang="nl">

<head>
    <?php require_once("headermeta.php"); ?>
</head>

<body>
<?php require_once("navbar.php"); ?>
    <div class="container">
    
    	<div id="output" class="alert alert-warning">No connection</div>
        
        <div class="panel panel-primary">
        <!-- Default panel contents -->
        <div class="panel-heading">
        	<button class="btn btn-default btn-small" onclick="autonomous()">let it roam free</button>
        	<button class="btn btn-default btn-small" onclick="control()">control it yourself</button>
        </div>
        <div class="panel-body">
            <p class="xform-p"></p>
            <p id="streamwrap" class="xform-p">
                <img id="streamimage" class="xform" src="http://192.168.0.220:9000/?action=stream" />
            </p>
				
		</div>
		</div>
		
<script>
var buttonPressed = "control";
 
function autonomous() {
	buttonPressed = "autonomous";
	//setupWebSocketConnection();
}	
function control() {
	buttonPressed = "control";
	//setupWebSocketConnection();
}

setupWebSocketConnection();

// Creates the websockets connection
function setupWebSocketConnection() {
	var $txt = $("#data"); // assigns the data(hostname/ip address) entered in the text box
	name = $txt.val(); // Variable name contains the string(hostname/ip address) entered in the text box
	var host = "ws://"+name+":9093/ws"; // combines the three string and creates a new string
	var socket = new WebSocket(host);
	var $txt = $("#data");
	var $btnSend = $("#sendtext");
	$txt.focus();
	
	// event handlers for UI
	$btnSend.on('click', function()
	{
		var text = $txt.val();
		if(text == "")
		{
			return;
		}
		$txt.val("");
	});
	$txt
	.keypress(function(evt)
	{
		if(evt.which == 13)
		{
			$btnSend.click();
		}
	});
	// event handlers for websocket
	if(socket)
	{
		var count =1;
		socket.onopen = function()
		{
			
			showServerResponse("The connection has been opened.");
			count = 0;
			arrows(); // function for detecting keyboard presses
			buttons(); // function for detecting the button press on webpage
		}
		//Send the button pressed backed to the Raspberry Pi
		function buttons()
		{
			if(buttonPressed == "autonomous"){
				socket.send("autonomous")
			}
			else if(buttonPressed == "control"){
				socket.send("control")
			}
		}
		function arrows()
		{
			document.onkeydown = KeyCheck;
			function KeyCheck()
			{
				var KeyID = event.keyCode;
				switch(KeyID)
				{
				case 16:
				socket.send("b");
				break;
				case 17:
				socket.send("b");
				break;
				case 37:
				socket.send("left");
				break;
				case 38:
				socket.send("forward");
				break;
				case 39:
				socket.send("right");
				break;
				case 40:
				socket.send("stop");
				break;
				}
			}
		}
		socket.onmessage = function(msg)
		{
			showServerResponse(msg.data);
		}
		socket.onclose = function()
		{
			//alert("connection closed....");
			showServerResponse("The connection has been closed.");
		}
	}
	else
	{
		showServerResponse("ERROR!!!");
		console.log("invalid socket");
	}
	function showServerResponse(txt)
	{
		var p = document.createElement('p');
		document.getElementById('output').innerHTML = ""
		p.innerHTML = txt;
		document.getElementById('output').appendChild(p);
	}	
}   
</script>
</body>


</div>
    <?php require_once("footer.php"); ?>
</div>
</div>


</html>
<script> jQuery(function($) {
  if (!("WebSocket" in window))
  {
    alert("Your browser does not support web sockets");
  }
});
</script>
