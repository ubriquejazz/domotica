// Called after form input is processed
function startConnect() {
	document.getElementById("boilerStatus").style.color="#3d434c";
	// TODO:
}

// Called when the client connects
function onConnect() {
	document.getElementById("boilerStatus").style.color="#3d434c";
    // TODO: 
}

// Called when the client loses its connection
function onConnectionLost(responseObject) {
    document.getElementById("messages").innerHTML += '<span>ERROR: Connection lost</span><br/>';
    if (responseObject.errorCode !== 0) {
        document.getElementById("messages").innerHTML += '<span>ERROR: ' + + responseObject.errorMessage + '</span><br/>';
    }
}

// Called when a message arrives
function onMessageArrived(message) {
    console.log("onMessageArrived: " + message.payloadString);
	topic = message.destinationName;
	value = message.payloadString;
	var date = new Date();
    document.getElementById("messages").innerHTML +=
		'<span>'+ date.getFullYear() + "/" + (date.getMonth() + 1) + "/" + date.getDate() +
		"-" + date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds() + ": " +
		topic + '  | ' + value + '</span><br/>';
    
    // TODO:
}

// set temperature
function setUserTemp(){
	document.getElementById("boilerStatus").style.color="#3d434c";
}

// set temperature
function setBackTemp(){
	document.getElementById("boilerStatus").style.color="#3d434c";
}

// set time
function setStartTime(){
	document.getElementById("boilerStatus").style.color="#3d434c";
}

// set time
function setStopTime(){
    document.getElementById("boilerStatus").style.color="#3d434c";
}

// Called when the disconnection button is pressed
function startDisconnect() {
	document.getElementById("boilerStatus").style.color="#3d434c";
}

// Updates #messages div to auto-scroll
function updateScroll() {
    var element = document.getElementById("messages");
    element.scrollTop = element.scrollHeight;
}
