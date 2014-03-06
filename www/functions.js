var winW, winH;
//var ball;
var ball1;
var ball2;
var points = [[]];
/*points[0][0] = 155;
points[0][1] = 245;
points[1][0] = 346;
points[1][1] = 248;
points[2][0] = 344; 
points[2][1] = 144;
points[3][0] = 414;
points[3][1] = 111;
points[4][0] = 408;
points[4][1] = 59;*/


function showPosition() {
 var s = 'X=' + window.event.clientX + ' Y=' + window.event.clientY;

 alert(s);


}
/*function vraagStraal() {
	//drawCirle(parseInt(prompt("Please enter radius rond AP1")));
	var str = prompt("Geef stralen seperated by ','");
	var res = str.split(",")
	drawCircle(res)
} 
 */
function drawCircle(str,str1,str2,str3) {
  //  var res = str.split(",")
	var surface = document.getElementById('surface');
    winW = surface.offsetWidth;
    winH = surface.offsetHeight;
    surface.width = winW;
    surface.height = winH;	
	//alert(str);
	ball1 = {radius: str,
        x: 136,
        y: 318,
        color: 'rgba(79, 79, 84, 0.4)'};
    var context = surface.getContext("2d");
	renderCircle(context, ball1);
	ball2 = {radius: str1,
        x: 228,
        y: 297,
        color: 'rgba(79, 79, 84, 0.4)'};
	var context = surface.getContext("2d");
	renderCircle(context, ball2);	
	ball3 = {radius: str2,
	
        x: 316,
        y: 268,
        color: 'rgba(79, 79, 84, 0.4)'};
	var context = surface.getContext("2d");
	renderCircle(context, ball3);	
	ball4 = {radius: str3,
        x: 316,
        y: 410,
        color: 'rgba(79, 79, 84, 0.4'};
	var context = surface.getContext("2d");
	renderCircle(context, ball4);	
	ball5 = {radius: 13.5,
        x: 17,
        y: 676,
        color: 'rgba(0, 0, 0, 0.2)'};
	var context = surface.getContext("2d");
	renderCircle(context, ball5);
  
	
}

function timedRefresh(timeoutPeriod) {
	setTimeout("location.reload(true);",timeoutPeriod);
}
/*function drawCirle2(radius) {
	var surface = document.getElementById('surface');
    winW = surface.offsetWidth;
    winH = surface.offsetHeight;
    surface.width = winW;
    surface.height = winH;
	
	ball2 = {radius: radius,
        x: 346,
        y: 248,
        color: 'rgba(0, 0, 0, 0.2)'};
	var context = surface.getContext("2d");
	renderCircle(context, ball2);
}
	*/

function renderCircle(context, ball) {
    context.beginPath();
    context.arc(ball.x, ball.y, ball.radius, 0, 2 * Math.PI, false);
    context.fillStyle = ball.color;
    context.fill();
    context.strokeStyle = ball.color;
    context.stroke();
}
