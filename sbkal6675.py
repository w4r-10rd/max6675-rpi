import paho.mqtt.client as mqtt

# MQTT broker and topic information
broker_address = "test.mosquitto.org"  # Use the test.mosquitto.org MQTT broker
port = 1883  # Default MQTT port
topic_prefix = "temperaturepi3b"  # Replace with your desired topic prefix

# Callback function to handle incoming messages
def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode("utf-8")

    # Extract the temperature value from the topic
    _, _, data_type = topic.rpartition("/")
    if data_type == "actual_temperature":
        print(f"Actual Temperature: {payload}")
    elif data_type == "filtered_temperature":
        print(f"Filtered Temperature: {payload}")

# Create an MQTT client
client = mqtt.Client("SensorSubscriber")

# Set up callback functions
client.on_message = on_message

# Connect to the MQTT broker
client.connect(broker_address, port)

# Subscribe to topics
client.subscribe(f"{topic_prefix}/sensor_data/actual_temperature")
client.subscribe(f"{topic_prefix}/sensor_data/filtered_temperature")

# Start the MQTT loop to listen for incoming messages
client.loop_forever()
