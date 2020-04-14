import paho.mqtt.client as mqtt
import datetime
import json
import ssl
import logging, traceback
import sys
import time

# Port for Mosquitto connection
PORT = 1883
# Port for AWS connection
SSL_PORT = 443

# Mosquitto broker address
mosq_broker = "test.mosquitto.org"
# Mosquitto client ID (Random string)
mosq_client_id = "e275e7835e404b4a7ca"

# ALPN protocol name (AWS)
IoT_protocol_name = "x-amzn-mqtt-ca"
# AWS broker address
aws_broker = "aws.broker.example.com"
# AWS client ID (Configured in AWS policies)
aws_client_id = "AWS_Client_ID_Example"

# CA certificate path
ca = "C:/your/path/to/cartificate/cert_name.pem"
# Client certificate path
cert = "C:/your/path/to/cartificate/cert_name.pem.crt"
# Private Key path
private = "C:/your/path/to/key/key_name.pem.key"

# Variable to define if a message must be sent
msg_ready = False
# Message to be sent
msg_to_be_sent = ""

# Topic to which the data will be published and received from
topic = "/topic/to/publish/example"

# Callback for Mosquitto connection
def on_connect_mosq(client, userdata, flags, rc):
	# Message to state a connection
	print("Connected to Mosquitto with result code " + str(rc))

	# Subscribe to Mosquitto topic to which the data will be
	# published by Arduino
	client.subscribe(topic)

# Callback for when a message is received from Mosquitto
def on_message_mosq(client, userdata, msg):
	global msg_ready
	global msg_to_be_sent

	# Sets the message to be sent as ready
	msg_ready = True
	# Sets the message to be sent
	msg_to_be_sent = msg.payload

# Sets the SSL configuration for a secure connection
def ssl_alpn():
    try:
        # Creates an SSL context
        ssl_context = ssl.create_default_context()
		# Sets the AWS protocol for ALPN
        ssl_context.set_alpn_protocols([IoT_protocol_name])
		# Sets the CA certificate
        ssl_context.load_verify_locations(cafile = ca)
		# Sets the client certificate and the private key
        ssl_context.load_cert_chain(certfile= cert, keyfile = private)

		# Returns the SSL context to be configured into MQTT
        return  ssl_context

    except Exception as e:
        print("exception ssl_alpn()")
        raise e

if __name__ == '__main__':

	try:
		# Creates the Mosquitto MQTT aws_client
		mosq_client = mqtt.Client(mosq_client_id)
		# Sets the callbacks
		mosq_client.on_connect = on_connect_mosq
		mosq_client.on_message = on_message_mosq

		# Connects to Mosquitto
		mosq_client.connect(mosq_broker, PORT)

		# Creates the AWS MQTT client
		aws_client = mqtt.Client(aws_client_id)
		# Configures the SSL context
		ssl_ctx = ssl_alpn()
		# Sets the SSL context
		aws_client.tls_set_context(context = ssl_ctx)
		# Connects to AWS
		aws_client.connect(aws_broker, port = SSL_PORT)

		# Starts both MQTT connections
		aws_client.loop_start()
		print("Connected to AWS")
		mosq_client.loop_start()

		while True:

			# When a message is received
			if True == msg_ready:
				# Sets the message as sent
				msg_ready = False
				print("Publish")
				# Publishes the message to Topic in AWS
				aws_client.publish(topic, msg_to_be_sent)

	# Exception to exit at CTRL + C
	except KeyboardInterrupt:
		# Disconnects from both servers
		aws_client.disconnect()
		print("Disconnected from AWS")
		mosq_client.disconnect()
		print("Disconnected from Mosquitto")

		print("END")
