import json
import paho.mqtt.client as mqtt

ubidots_broker = "industrial.api.ubidots.com"
PORT = 1883
client_id = "LAMBDA_PUB"
topic = "/v1.6/devices/357520077334163"

message = '{"temp":10,"hum":10,"lum":10}'

connect = False

def on_connect(client, userdata, flags, rc):
	global connect

	connect = True

def lambda_handler(event, context):

	ubi_client = mqtt.Client(client_id)
	ubi_client.username_pw_set("BBFF-mimwlgWwTC29aKimKv0jOU57SVNikeEK6J58eJqeibsoxMtNgqoFA4m")
	ubi_client.connect(ubidots_broker, PORT)

	while not connect:
		a = 1

	ubi_client.publish(topic, message)

    # TODO implement
	return {'statusCode': 200, 'body': json.dumps('Hello from Lambda!')}
