import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 3900000

try:
    while 1:

        t = spi.readbytes(2)
        time.sleep(0.5)

        msb = format(t[0], '#010b')
        lsb = format(t[1], '#010b')

        r_temp = msb[2:] + lsb[2:]
        t_bytes = "0b" + r_temp[0:13]
        temp = int(t_bytes, base=2)*0.25
        print("Temperatura: {:.2f} ºC".format(temp))
except KeyboardInterrupt:
    print("Publisher stopped by user.")
