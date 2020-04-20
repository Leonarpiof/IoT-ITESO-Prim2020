import json
import requests
import time
import boto3

# Ubidots access token
TOKEN = "BBFF-mimwlgWwTC29aKimKv0jOU57SVNikeEK6J58eJqeibsoxMtNgqoFA4m"
# Ubidots stem address
address = "http://industrial.api.ubidots.com"

# Passwords to decrypt the message
temp_pswd = 0x4D3
hum_pswd = 0x6FA
lum_pswd = 0xC37B8

# Object to manage DynamoDB
dynamodb = boto3.resource('dynamodb')
# Object to manage the table IoT_DB
table = dynamodb.Table('IoT_DB')

# Posts via HTTP to ubidots
def post_request(payload, device_label):
	# sets the address and the label to the URL
	url = "{}/api/v1.6/devices/{}".format(address, device_label)
	# Headers for the post request
	headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

	# Status of the post request
	status = 400
	# Number of attempts to post
	attempts = 0

	# If the status is not successful, tries to post_request
	# 5 times
	while status >= 400 and attempts <= 5:
		# Post request
		req = requests.post(url=url, headers=headers, json=payload)
		# Gets the request status
		status = req.status_code
		# Retries in 1 second
		attempts += 1
		time.sleep(1)

	# If could not publish in 5 trues, returns error
	if status >= 400:
		return False

	# Otherwise, returns success
	return True

# Lambda function handler
def lambda_handler(event, context):
	# Dictionary to be sent to Ubidots with error values
	msg_to_be_sent = {"temp":"value": -1, "hum":-1, "lum":-1}

	# Decrypts the messages
	event["temp"] ^= temp_pswd
	event["hum"] ^= hum_pswd
	event["lum"] ^= lum_pswd

	# Sets the dictionary to be sent to Ubidots
	msg_to_be_sent["temp"] = event["temp"]
	msg_to_be_sent["hum"] = event["hum"]
	msg_to_be_sent["lum"] = event["lum"]

	# Puts data received into DynamoDB
	table.put_item(Item = event)

	# Publishes the message to ubidots via HTTP, to the proper device
	post_request(msg_to_be_sent, event["IMEI"])

    # Return value
	return {'statusCode': 200, 'body': json.dumps(msg_to_be_sent)}
