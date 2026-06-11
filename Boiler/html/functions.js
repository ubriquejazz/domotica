var client = null;

var MQTT_SERVER = window.APP_CONFIG.infra.mqtt_server;

// Topic definitions mapped from config.json
var PREFIX_SET    = window.APP_CONFIG.infra.topic_params_set_prefix;    // "home/params/set/"
var PREFIX_STATUS = window.APP_CONFIG.infra.topic_params_get_prefix;    // "home/params/status/"
var T_PARAMS_GET  = window.APP_CONFIG.infra.topic_params_get;           // "home/params/get"
var T_RELAY_GET   = window.APP_CONFIG.infra.topic_relay_status;         // "home/relay/status"
var T_RELAY_SET   = window.APP_CONFIG.infra.topic_relay_set;           // "home/relay/set"

// Called after form input is processed
function startConnect() {
    document.getElementById("boilerStatus").style.color = "#3d434c";

    // Generate a unique client ID to prevent broker collision disconnects
    var clientID = "boiler-frontend-" + parseInt(Math.random() * 1000);
    var port = "8080"; 

    // Log connection updates directly to the UI messages div
    var messagesDiv = document.getElementById("messages");
    if (messagesDiv) {
        messagesDiv.innerHTML += '<span>Connecting to: ' + MQTT_SERVER + ' on port: ' + port + '</span><br/>';
        messagesDiv.innerHTML += '<span>Client ID allocated: ' + clientID + '</span><br/>';
    }

    // Initialize the Paho client running over WebSockets
    client = new Paho.MQTT.Client(MQTT_SERVER, MQTT_PORT, clientID);
    client.onConnectionLost = onConnectionLost;
    client.onMessageArrived = onMessageArrived;

    var options = {
        onSuccess: onConnect
    };

    // Safely apply authentication if defined in config.json
    if (window.APP_CONFIG.infra.mqtt_user && window.APP_CONFIG.infra.mqtt_pass) {
        options.userName = window.APP_CONFIG.infra.mqtt_user;
        options.password = window.APP_CONFIG.infra.mqtt_pass;
    }

    client.connect(options);
}

// Called when the client connects
function onConnect() {
    console.log("MQTT Broker Connection Successful.");
    
    document.getElementById("boilerStatus").style.color = "#3d434c";

    // Print output for the user in the messages div
    var messagesDiv = document.getElementById("messages");
    messagesDiv.innerHTML += '<span>Subscribing to: home/#</span><br/>';

    // Subscribe using the dynamic topics from config.json
    client.subscribe(PREFIX_STATUS + "#"); 
    client.subscribe(T_RELAY_SET);

    // Send a empty trigger command to sync UI elements with the hardware's active profile
    var getMessage = new Paho.MQTT.Message(" ");
    getMessage.destinationName = T_PARAMS_GET;
    client.send(getMessage);
    
    // Send update commands
    var message1 = new Paho.MQTT.Message("OFF");
    message1.destinationName = T_RELAY_SET;
    client.send(message1);
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

// Called when the disconnection button is pressed
function startDisconnect() {
    document.getElementById("boilerStatus").style.color = "#3d434c";
    client.disconnect();
    document.getElementById("messages").innerHTML += '<span>Disconnected</span><br/>';
}

// Updates #messages div to auto-scroll
function updateScroll() {
    var element = document.getElementById("messages");
    element.scrollTop = element.scrollHeight;
}

// userTempSelect, backTempSelect
function setUserTemp(){
	document.getElementById("boilerStatus").style.color="#3d434c";
	var sel = Number(document.getElementById("userTempSelect").value) + 16;
	message = new Paho.MQTT.Message(sel.toString());
	message.destinationName = "home/params/set/user_temp";
	client.send(message);
}

function setBackTemp(){
	document.getElementById("boilerStatus").style.color="#3d434c";
	var sel = Number(document.getElementById("backTempSelect").value) + 14;
	message = new Paho.MQTT.Message(sel.toString());
	message.destinationName = "home/params/set/back_temp";
	client.send(message);
}

// startTimeSelect, stopTimeSelect
function setStartTime(){
	document.getElementById("boilerStatus").style.color="#3d434c";
	var sel = document.getElementById("startTimeSelect").value;
	message = new Paho.MQTT.Message(sel);
	message.destinationName = "home/params/set/start_time";
	client.send(message);
}

function setStopTime(){
	document.getElementById("boilerStatus").style.color="#3d434c";
	var sel = document.getElementById("stopTimeSelect").value;
	message = new Paho.MQTT.Message(sel);
	message.destinationName = "home/params/set/stop_time";
	client.send(message);
}
