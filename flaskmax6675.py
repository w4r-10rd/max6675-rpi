import time
from flask import Flask, render_template, jsonify

import spidev  # Import the spidev module

app = Flask(__name__)

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 3900000

def read_max6675_temperature(spi):
    t = spi.readbytes(2)
    msb = format(t[0], '#010b')
    lsb = format(t[1], '#010b')
    r_temp = msb[2:] + lsb[2:]
    t_bytes = "0b" + r_temp[0:13]
    temp = int(t_bytes, base=2) * 0.25
    return temp

def read_temp():
    temperature_from_max6675 = read_max6675_temperature(spi)
    return temperature_from_max6675

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/temperature')
def get_temperature():
    temperature = read_temp()
    return jsonify({'temperature': temperature})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
