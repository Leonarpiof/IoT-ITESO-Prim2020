import json
import requests
import time

# Ubidots access token
TOKEN = "BBFF-mimwlgWwTC29aKimKv0jOU57SVNikeEK6J58eJqeibsoxMtNgqoFA4m"
# Device's label
DEVICE_LABEL = "357520077334163"
# Ubidots stem address
address = "http://industrial.api.ubidots.com"

# Message to be published
#message = {'temp':25,'hum':40,'lum':8000}

# XOR password
pswd = [43, 137, 1, 171, 45, 180, 76, 95, 44, 88, 180,
	24, 255, 62, 157, 171, 24, 163, 154, 4, 179,
	122, 157, 33, 144, 239, 62, 63, 210, 123, 60,
	176, 108, 232, 175, 144, 250, 68, 85, 64, 138,
	182, 172, 4, 222, 11, 23, 94, 62, 83, 51, 150,
	72, 69, 211, 23, 227, 6, 50, 222, 194, 31, 225,
	164, 134, 114, 199, 219, 47, 79, 56, 35, 87,
	207, 80, 139, 8, 213, 84, 116, 140, 160, 140,
	46, 84, 151, 126, 251, 83, 128, 146, 252, 31,
	78, 197, 23, 252, 150, 227, 5]

# Posts via HTTP to ubidots
def post_request(payload):
	# sets the address and the label to the URL
	url = "{}/api/v1.6/devices/{}".format(address, DEVICE_LABEL)
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

# Builds message from encryped one
def build_message(event):
	# Counter for the password
	i = 0
	# Variable to store the message
	xored_msg = ""
	# For each character in the message
	for value in event("recol_data"):
		# Gets its ASCII value
		ascii = ord(value)
		# XOR with password
		xored_msg += chr(ascii ^ pswd[i])
		i += 1

	# Formats the string into a python dictionary
	xored_msg = json.loads(xored_msg)

	# Returns the string
	return xored_msg


# Lambda function handler
def lambda_handler(event, context):
	# Gets the encrypted message
	message = build_message(event)

	# Publishes the message to ubidots via HTTP
	post_request(message)

    # Return value
	return {'statusCode': 200, 'body': json.dumps('Hello from Lambda!')}
