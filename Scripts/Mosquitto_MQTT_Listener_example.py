import paho.mqtt.client as mqtt

# Mosquitto no TLS port
PORT = 1883
# Mosquitto broker address
broker = "test.mosquitto.org"
# Mosquitto client ID (Random string)
client_id = "5fna2sh5dbF5sq412dafslkjKJFSD3AJ"

# Topic to which the data will be published and received from
topic = "/test/topic"
# MQTT client object
mosq_client = mqtt.Client(client_id)

# Connect to server callback
def on_connect(client, userdata, flags, rc):
	global connect

	# Subscribes to topic
	client.subscribe(topic)

# Receive message callback
def on_message(client, userdata, msg):
	# Print the message payload
	print(msg.payload)

if __name__ == '__main__':
	try:
		# Sets both callbacks
		mosq_client.on_connect = on_connect
		mosq_client.on_message = on_message
		# Connects to Mosquitto broker
		mosq_client.connect(broker, PORT)
		# Initializes connection
		mosq_client.loop_start()

		# Waits for messages to arrive
		while True:
			a = 1

	# Ends process at CTRL + C
	except KeyboardInterrupt:
		# Disconnects from broker
		mosq_client.disconnect()
		print("END")
