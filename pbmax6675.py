import paho.mqtt.client as mqtt
import time
import spidev

# MQTT broker and topic information
broker_address = "192.168.0.131"  # Use the test.mosquitto.org MQTT broker
port = 1883  # Default MQTT port
topic_prefix = "temperaturepi3b"  # Replace with your desired topic prefix

# Create an MQTT client
client = mqtt.Client("SensorPublisher")

# SPI initialization for Max6675
spi = spidev.SpiDev()
try:
    spi.open(0, 0)
    spi.max_speed_hz = 3900000
except Exception as e:
    print("Error initializing SPI:", e)
    exit(1)

def read_temp():
    try:
        t = spi.readbytes(2)

        msb = format(t[0], '#010b')
        lsb = format(t[1], '#010b')

        r_temp = msb[2:] + lsb[2:]
        t_bytes = "0b" + r_temp[0:13]
        temp = int(t_bytes, base=2) * 0.25
        return temp
    except Exception as e:
        print("Error reading temperature:", e)
        return None

# Callback function for when a message is received from the broker
def on_message(client, userdata, message):
    pass  # Do nothing for received messages

try:
    # Connect to the MQTT broker
    client.connect(broker_address, port)
    print("Connected to MQTT broker.")

    # Subscribe to the topic where temperature data is published with QoS level 1
    client.subscribe(f"{topic_prefix}/sensor_data/actual_temperature", qos=1)

    # Set the callback function for message reception
    client.on_message = on_message

    # Start the loop to listen for incoming messages
    client.loop_start()

    while True:
        # Publish actual temperature to specific topic
        temperature = read_temp()
        if temperature is not None:
            client.publish(f"{topic_prefix}/sensor_data/actual_temperature", f"{temperature:.2f} °C")
            print(f"Published Actual Temperature: {temperature:.2f} °C")
        else:
            print("Temperature reading failed.")

        time.sleep(1)  # Add a n-second delay

except KeyboardInterrupt:
    print("Publisher stopped by user.")

except Exception as e:
    print("An error occurred:", e)

finally:
    # Stop the MQTT loop and disconnect from the broker
    client.loop_stop()
    client.disconnect()
    print("Disconnected from MQTT broker.")
  
