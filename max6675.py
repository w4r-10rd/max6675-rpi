import spidev
import time

# Set up SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # You may need to adjust the bus and device based on your hardware setup

# Function to read temperature from MAX6675
def read_temperature():
    try:
        # Read raw data from MAX6675
        adc_data = spi.xfer2([0x00, 0x00])

        # Combine the two bytes into a 12-bit value
        raw_value = ((adc_data[0] & 0b1111111) << 8) | adc_data[1]

        # Convert to temperature (assuming Celsius)
        temperature = raw_value * 0.25

        return temperature

    except KeyboardInterrupt:
        spi.close()
        exit()

# Main loop
try:
    while True:
        temperature = read_temperature()
        print(f"Temperature: {temperature} °C")
        time.sleep(1)  # Adjust the delay as needed

except KeyboardInterrupt:
    spi.close()
