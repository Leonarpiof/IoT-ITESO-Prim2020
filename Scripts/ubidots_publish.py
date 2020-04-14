import json
import paho.mqtt.client as mqtt
import time

# Ubidots Stem broker
ubidots_broker = "industrial.api.ubidots.com"
# Por for non-TLS connections
PORT = 1883
# Client ID
client_id = "Client_ID_EXAMPLE"
# Topic to which the data will be publised
# The Ubidots topic has the following format:
# /v1.6/devices/ + device label, set in Ubidots by the user
topic = "/v1.6/devices/device_label"
# Token given by ubidots to publish into the devices
# (Ubidots App)
TOKEN = "ubidots_token"

# Strings for the JSON format
temp = '{"temp":'
hum = ',"hum":'
lum = ',"lum":'
end = '}'

# Variable for the message to be sent
msg = ""

# Variables' values
temperature = 150
humidity = 650
luminosity = 25000

# Defines whether the client is connected or not
connect = False
# MQTT client object
ubi_client = mqtt.Client(client_id)

# Connect to broker callback
def on_connect(client, userdata, flags, rc):
	global connect

	# Sets the client as connected
	connect = True

if __name__ == '__main__':

	try:
		# Sets the callabak
		ubi_client.on_connect = on_connect
		# Sets the username credential
		ubi_client.username_pw_set(TOKEN)
		# Connects to broker
		ubi_client.connect(ubidots_broker, PORT)
		# Begins connection
		ubi_client.loop_start()

		# Waits for the client to be connected
		while not connect:
			a = 1

		while True:
			# Each iteration, adds 0.1°C to the temperature
			# If the temperature reaches 16°C, goes back to 15°C
			temperature += 1
			if(temperature >= 160):
				temperature = 150

			# Each iteration, subtracts 0.1% RH to the humidity
			# If the humidity reaches 63% RH, goes back to 65% RH
			humidity -= 1
			if(humidity <= 630):
				humidity = 650

			# Each iteration, adds 100 lx to the luminosity
			# If the luminosity reaches 27000 lx, goes back to 25000 lx
			luminosity += 100
			if(luminosity >= 27000):
				luminosity = 25000

			# Builds the JSON string
			msg = temp + str(temperature) + hum + str(humidity) + lum + str(luminosity) + end

			# Prints the message
			print("Publish: " + msg)
			# Publishes the message in MQTT
			ubi_client.publish(topic, msg)
			# Sleeps for 5 min
			time.sleep(300)

	# Ends program at CTRL + C
	except KeyboardInterrupt:
		print("END")
