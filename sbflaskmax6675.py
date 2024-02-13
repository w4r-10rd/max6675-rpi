import paho.mqtt.client as mqtt
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# MQTT broker and topic information
broker_address = "192.168.0.131"
port = 1883
topic_prefix = "temperaturepi3b"

# Callback function to handle incoming messages
def on_message(client, userdata, message):
    # Extract numerical value from temperature string
    temperature_str = message.payload.decode()
    temperature_value = float(temperature_str.split()[0])
    socketio.emit('temperature_update', {'temperature': temperature_value}, namespace='/temperature')

# Create an MQTT client
client = mqtt.Client("SensorSubscriber")

# Set callback function
client.on_message = on_message

# Connect to the MQTT broker
client.connect(broker_address, port)

# Subscribe to the topic where temperature data is published
client.subscribe(f"{topic_prefix}/sensor_data/actual_temperature")

# Start the MQTT loop in a separate thread
client.loop_start()

# Route for serving the HTML dashboard
@app.route('/')
def index():
    return render_template('dashboard.html')

# WebSocket event handler for receiving temperature updates
@socketio.on('connect', namespace='/temperature')
def test_connect():
    print('Client connected')

# Start the Flask-SocketIO server
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
