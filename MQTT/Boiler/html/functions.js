// Called after form input is processed
function startConnect() {
    document.getElementById("boilerStatus").style.color = "#3d434c";

    // Generate a random client ID
    var clientID = "clientID-" + parseInt(Math.random() * 1000);

    // Fetch the hostname/IP address and port number from the form
    var host = "192.168.1.100"; //document.getElementById("host").value;
    var port = "8080"; 			//document.getElementById("port").value;

    // Print output for the user in the messages div
    var messagesDiv = document.getElementById("messages");
    messagesDiv.innerHTML += '<span>Connecting to: ' + host + ' on port: ' + port + '</span><br/>';
    messagesDiv.innerHTML += '<span>Using the following client value: ' + clientID + '</span><br/>';

    // Initialize new Paho client connection, callback handlers
    var client = new Paho.MQTT.Client(host, Number(port), clientID);
    client.onConnectionLost = onConnectionLost;
    client.onMessageArrived = onMessageArrived;

    // Connect the client, if successful, call onConnect function
    client.connect({
        onSuccess: onConnect,
    });
}

// Called when the client connects
function onConnect() {
    document.getElementById("boilerStatus").style.color = "#3d434c";

    // Print output for the user in the messages div
    var messagesDiv = document.getElementById("messages");
    messagesDiv.innerHTML += '<span>Subscribing to: home/#</span><br/>';

    // Subscribe to the requested topic
    client.subscribe("home/#");

    // Send update commands
    var message1 = new Paho.MQTT.Message("1");
    message1.destinationName = "home/relay/get";
    client.send(message1);

    var message2 = new Paho.MQTT.Message("1");
    message2.destinationName = "home/params/get";
    client.send(message2);
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
    // Log the received message payload to the console
    console.log("onMessageArrived: " + message.payloadString);
    
    // Extract topic and payload value from the message
    var topic = message.destinationName;
    var value = message.payloadString;
    
    // Get the current date and time
    var date = new Date();
    
    // Append message information to the messages element
    var messagesDiv = document.getElementById("messages");
    messagesDiv.innerHTML +=
        '<span>' + date.getFullYear() + "/" + (date.getMonth() + 1) + "/" + date.getDate() +
        "-" + date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds() + ": " +
        topic + '  | ' + value + '</span><br/>';

    // Call the updateScroll function
    updateScroll();
    
    // Update specific HTML elements based on the received topic and value
    switch (topic) {
        case "home/params/status/start_time":
            document.getElementById("startTime").innerHTML = value;
            break;
        case "home/params/status/stop_time":
            document.getElementById("stopTime").innerHTML = value;
            break;
        case "home/params/status/user_temp":
            document.getElementById("userTemp").innerHTML = value + ' ºC';
            break;
        case "home/params/status/back_temp":
            document.getElementById("backTemp").innerHTML = value + ' ºC';
            break;
        case "home/params/status/curr_temp":
            document.getElementById("currentTemp").innerHTML = value + ' ºC';
            break;
        case "home/relay/status":
            document.getElementById("boilerStatus").innerHTML = value;
            if (value == "OFF") {
                document.getElementById("boilerStatus").style.color = "#dd0000";
            } else if (value == "ON") {
                document.getElementById("boilerStatus").style.color = "#00dd00";
            } else {
                document.getElementById("boilerStatus").style.color = "#3d434c";
            }
            break;
        default:
            // Handle other topics if needed
            break;
    }
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
