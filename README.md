# max6675-k_rpi_IIOT-Framework
_max6675k connected with raspberrypi to enact as a complete temperature analysis solution._

This repository is for those framework that has or uses MAX6675-K module for its operation.

templates -> this directory contains the ui html files

flaskmax6675.py -> visualizes obtained data in a localhost/0.0.0.0 dashboard ui

max6675.py -> a basic code to acquire temperature data via max6675k module.

pbadvmax6675.py -> mqtt publisher with qos services

pbkal6675.py -> mqtt publisher with kalman filter over obtained sensor data

pbmax6675.py -> mqtt publisher for max6675 rpi frmaework

sbflaskmax6675.py -> its a flask env which tends to subscribe to a max6675 mqtt publisher where the data obtained gets visualized in a localhost/0.0.0.0 dashboard ui

sbkal6675.py -> subscriber to publisher with kalman filter

sbmaxx6675.py -> its a simple mqtt publisher subscriber that displays the data as obtained with respected to delay in the framework


**All rights reserved to the repository owner.**
