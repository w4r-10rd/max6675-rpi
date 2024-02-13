import paho.mqtt.client as mqtt

# Callback function for when a message is received from the broker
def on_message(client, userdata, message):
    print("Received message:", str(message.payload.decode("utf-8")))

# MQTT broker and topic information
broker_address = "test.mosquitto.org"  # Use the test.mosquitto.org MQTT broker
port = 1883  # Default MQTT port
topic = "temperaturepi3b/sensor_data/actual_temperature"

# Create an MQTT client
client = mqtt.Client("SensorSubscriber")

# Set the callback function for message reception
client.on_message = on_message

try:
    # Connect to the MQTT broker
    client.connect(broker_address, port)
    print("Connected to MQTT broker.")

    # Subscribe to the topic
    client.subscribe(topic)

    # Start the loop to listen for incoming messages
    client.loop_forever()

except KeyboardInterrupt:
    print("Subscriber stopped by user.")

except Exception as e:
    print("An error occurred:", e)

finally:
    # Disconnect from the broker
    client.disconnect()
    print("Disconnected from MQTT broker.")
