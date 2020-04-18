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
Contains the Lambda deploy package, which has the lambda function handler, and the necessary libraries for the project to work, that are not included in AWS Lambda. Developed in Python 3.8

### Schematics
Contains the schematics made for the project, and other PCB related files, such as the board file and the BOM.

### Scripts
Contains Python scripts to test different elements such as Ubidots, Mosquitto, and other features. For this scripts to work, it is necessary to install paho-mqtt and requests. Scripts developed in Python 3.8.1