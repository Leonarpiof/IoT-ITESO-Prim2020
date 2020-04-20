# IoT-ITESO-Prim2020
This repo contains the documentation and generated files during the IoT project of spring 2020 at ITESO, by Leon Arpio Fernandez

## Folders
### Arduino
Contains the source code of the project, in which the sensors are read, and data is sent through cellular network, 
using MQTT. This project is made for the Arduino MKR GSM 1400.

This project uses the following libraries:
- [Arduino MKR GSM libraries](https://github.com/arduino-libraries/MKRGSM)
- [MQTT library for Arduino](https://github.com/256dpi/arduino-mqtt)
- [I2C Soil Moisture Sensor](https://github.com/Apollon77/I2CSoilMoistureSensor)

### Documentation
Contains the documentation made during the project, which contains the research plan, comparative tables, requirements, business model,
customer journey, and others. **All documentas are in Spanish**.

### Lambda
Contains the Lambda deploy package, which has the lambda function handler, and the necessary libraries for the project to work, that are not included in AWS Lambda. Developed in Python 3.8. For the Lambda deploy package download Python library [requests](https://requests.readthedocs.io/en/master/).

To install the library in a specific folder, navigate in the command line to the desired folder, and use the following command.

```
pip install requests -t .
```
- Download [pip](https://pip.pypa.io/en/stable/reference/pip_download/)

### Schematics
Contains the schematic, board file and BOM. Schematic based on [Arduino MKR GSM 1400 schematic](https://store.arduino.cc/usa/mkr-gsm-1400).


### Scripts
Contains Python scripts to test different elements such as Ubidots, Mosquitto, and other features. For this scripts to work, it is necessary to install paho-mqtt and requests. Scripts developed in Python 3.8.1

# Author
León Arpio Fernández
