from flask import Flask, jsonify, request
import serial
import time

app = Flask(__name__)

# Configuración del puerto serie
try:
    arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    time.sleep(2)  # Espera para inicializar la conexión
    print("Conexión con Arduino establecida.")
except Exception as e:
    arduino = None
    print(f"Error al conectar con Arduino: {e}")

# Ruta principal para comprobar el estado del servidor
@app.route('/')
def home():
    return jsonify({"message": "Servidor Flask en funcionamiento", "status": "OK"})

# Ruta para encender o apagar el LED
@app.route('/toggle-led', methods=['POST'])
def toggle_led():
    if not arduino:
        return jsonify({"error": "Arduino no está conectado"}), 500
    
    data = request.get_json()
    action = data.get('action', '').upper()
    
    if action == 'ON':
        arduino.write(b'LEDON\n')
    elif action == 'OFF':
        arduino.write(b'LEDOFF\n')
    else:
        return jsonify({"error": "Acción inválida, use 'ON' o 'OFF'"}), 400

    response = arduino.readline().decode().strip()
    return jsonify({"message": response})

# Ruta para obtener la temperatura
@app.route('/get-temp', methods=['GET'])
def get_temp():
    if not arduino:
        return jsonify({"error": "Arduino no está conectado"}), 500
    
    arduino.write(b'GET_TEMP\n')
    response = arduino.readline().decode().strip()
    
    if "Error" in response:
        return jsonify({"error": "No se pudo leer la temperatura"}), 500
    
    try:
        temperature = float(response.split(":")[1].strip(" °C"))
        return jsonify({"temperature": temperature})
    except Exception:
        return jsonify({"error": "Respuesta inesperada del Arduino"}), 500

# Ruta para verificar el estado del LED
@app.route('/led-status', methods=['GET'])
def led_status():
    if not arduino:
        return jsonify({"error": "Arduino no está conectado"}), 500
    
    arduino.write(b'STATUS\n')
    response = arduino.readline().decode().strip()
    return jsonify({"led_status": response})

# Ruta para verificar conexión con Arduino
@app.route('/check-arduino', methods=['GET'])
def check_arduino():
    if arduino and arduino.is_open:
        return jsonify({"message": "Arduino está conectado", "status": "connected"})
    else:
        return jsonify({"error": "Arduino no está conectado"}), 500

# Ejecutar el servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
