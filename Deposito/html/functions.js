var client = null;

// Called after form input is processed
function startConnect() {
    var status = document.getElementById("boilerStatus");
    status.style.color = "#f1c40f"; // Yellow
    status.innerText = "● Conectando...";

    // Generate a random client ID
    var clientID = "clientID-" + parseInt(Math.random() * 1000);
    var port = "8083";
    var host = window.APP_CONFIG.mqtt_server; 

    // Print output for the user in the messages div
    var messagesDiv = document.getElementById("messages");
    messagesDiv.innerHTML += '<span>Connecting to: ' + host + ' on port: ' + port + '</span><br/>';
    messagesDiv.innerHTML += '<span>Using the following client value: ' + clientID + '</span><br/>';

    // Initialize new Paho client connection, callback handlers
    client = new Paho.MQTT.Client(host, Number(port), clientID);
    client.onConnectionLost = onConnectionLost;
    client.onMessageArrived = onMessageArrived;

    // Connect the client, if successful, call onConnect function
    client.connect({
        userName: window.APP_CONFIG.mqtt_user,
        password: window.APP_CONFIG.mqtt_pass,
        onSuccess: onConnect,
    //    keepAliveInterval: 30, // Sends a ping every 30 seconds
    //    timeout: 3,            // Gives up on after 3 seconds
    });
}

function subscribe(topic) { 
    var messagesDiv = document.getElementById("messages");
    client.subscribe(topic);  
    messagesDiv.innerHTML += `<span>Subscribing to: ${topic}</span><br/>`;
}

// Called when the client connects
function onConnect() {
    var status = document.getElementById("boilerStatus");
    status.style.color = "#2ecc71"; // Green
    status.innerText = "● Conectado";

    subscribe(window.APP_CONFIG.topic_temp);
    // TODO: Add more subscribers
}

// Called when the client loses its connection
function onConnectionLost(responseObject) {
    var status = document.getElementById("boilerStatus");
    status.style.color = "#e74c3c"; // Red
    status.innerText = "● Desconectado";

    document.getElementById("messages").innerHTML += '<span>ERROR: Connection lost</span><br/>';
    if (responseObject.errorCode !== 0) {
        document.getElementById("messages").innerHTML += '<span>ERROR: ' + + responseObject.errorMessage + '</span><br/>';
    }
}

function debug_response(topic, value) {
    var date = new Date();
    var messagesDiv = document.getElementById("messages");
    messagesDiv.innerHTML +=
        '<span>' + date.getFullYear() + "/" + (date.getMonth() + 1) + "/" + date.getDate() +
        "-" + date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds() + ": " +
        topic + '  | ' + value + '</span><br/>';
}

// Called when a message arrives
function onMessageArrived(message) {
    var topic = message.destinationName;
    var value = message.payloadString;
    var lectura;
    debug_response(topic, value);
    var topicRecibido = topic.toString();
    if (topicRecibido === window.APP_CONFIG.topic_temp) {
        lectura = JSON.parse(message.payloadString);
        console.log("Temp y timestamp del RP2040.");
        document.getElementById("timestamp").innerHTML = lectura.count;
        updateTemperature(lectura.temp);
    }   
    // TODO: Add more subscribers  
    else {
        console.log("Topic desconocido: " + topicRecibido);
    }
}

// Called when the disconnection button is pressed
function startDisconnect() {
    var messagesDiv = document.getElementById("messages");
    messagesDiv.innerHTML += '<span>Disconnected</span><br/>';
    client.disconnect();
}

function updateTemperature(temperatura) {
    var tempNum = parseFloat(temperatura) % 100;
    if (isNaN(tempNum)) {
        console.error("Invalid value received:", temperatura);
        return; 
    }
    document.getElementById("temperatura").innerHTML = tempNum + " %";
    
    // Calculate and round colors using our clean number
    var color_R = Math.round((tempNum / 100.0) * 255);
    var color_B = Math.round(((100.0 - tempNum) / 100.0) * 255);
    document.getElementById("temp").style.backgroundColor = "rgb(" + color_R + ", 0, " + color_B + ")";
    
    // Update the progress bar width
    document.getElementById("temp").style.width = tempNum + "px";
}