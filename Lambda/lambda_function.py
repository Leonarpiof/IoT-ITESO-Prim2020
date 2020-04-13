import json
import requests
import time

TOKEN = "BBFF-mimwlgWwTC29aKimKv0jOU57SVNikeEK6J58eJqeibsoxMtNgqoFA4m"
DEVICE_LABEL = "357520077334163"
address = "http://industrial.api.ubidots.com"

message = {'temp':25,'hum':40,'lum':8000}

def post_request(payload):
	url = "{}/api/v1.6/devices/{}".format(address, DEVICE_LABEL)
	headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

	status = 400
	attempts = 0

	while status >= 400 and attempts <= 5:
		req = requests.post(url=url, headers=headers, json=payload)
		status = req.status_code
		attempts += 1
		time.sleep(1)
		print(status)

	# Processes results
	if status >= 400:
		print("[ERROR] Could not send data after 5 attempts, please check \
			\nyour token credentials and internet connection")
		return False

	print("[INFO] request made properly, your device is updated")
	return True

def lambda_handler(event, context):
	post_request(message)

    # TODO implement
	return {'statusCode': 200, 'body': json.dumps('Hello from Lambda!')}

lambda_handler("test", "test")
