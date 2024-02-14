import paho.mqtt.client as mqtt
import time
import spidev

# MQTT broker and topic information
broker_address = "192.168.0.130"  # Use the test.mosquitto.org MQTT broker
port = 1883  # Default MQTT port
topic_prefix = "temperaturepi3b"  # Replace with your desired topic prefix

# Create an MQTT client
client = mqtt.Client("SensorPublisher")

# Connect to the MQTT broker
client.connect(broker_address, port)

# SPI initialization for Max6675
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 3900000

# Kalman filter parameters for temperature
Q_temp = 0.01  # Process noise covariance
R_temp = 0.1   # Measurement noise covariance
x_temp = 30.0  # Initial estimate
P_temp = 1.0   # Initial error covariance

def kalman_filter(z, x, P, Q, R):
    # Prediction
    x_pred = x
    P_pred = P + Q

    # Update
    K = P_pred / (P_pred + R)
    x = x_pred + K * (z - x_pred)
    P = (1 - K) * P_pred

    return x, P

def read_temp():
    t = spi.readbytes(2)

    msb = format(t[0], '#010b')
    lsb = format(t[1], '#010b')

    r_temp = msb[2:] + lsb[2:]
    t_bytes = "0b" + r_temp[0:13]
    temp = int(t_bytes, base=2) * 0.25
    return temp

try:
    while True:
        temperature = read_temp()

        # Filter temperature
        filtered_temperature, P_temp = kalman_filter(temperature, x_temp, P_temp, Q_temp, R_temp)

        # Publish actual and filtered temperature to specific topics
        client.publish(f"{topic_prefix}/sensor_data/actual_temperature", f"{temperature:.2f} °C")
        client.publish(f"{topic_prefix}/sensor_data/filtered_temperature", f"{filtered_temperature:.2f} °C")

        print(f"Published Actual Temperature: {temperature:.2f} °C, Filtered Temperature: {filtered_temperature:.2f} °C")

        time.sleep(1)  # Add a n-second delay

except KeyboardInterrupt:
    print("Publisher stopped by user.")

# Disconnect from the broker
client.disconnect()
