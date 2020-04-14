import time
import requests
import math
import random

# Token given by ubidots to publish into the devices
# (Ubidots App)
TOKEN = "ubidots_given_token"
# Davice to which the data will be published
DEVICE_LABEL = "device_label"
# Ubidots URL
address = "http://industrial.api.ubidots.com"

# Variables values to be publised
temperature = 250
humidity = 630
luminosity = 15000

# Posts to Ubidots
def post_request(payload):
	# Sets the complete URL to post data
	url = "{}/api/v1.6/devices/{}".format(address, DEVICE_LABEL)
	# Authentication header
	headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

	# Variable for the POST status (400 = POST request rejected)
	status = 400
	# Number of attempts to post
	attempts = 0

	# Tries 5 times to post successfuly
	while status >= 400 and attempts <= 5:
		# POST request
		req = requests.post(url=url, headers=headers, json=payload)
		# Retrieves the request statys
		status = req.status_code
		# Waits for one second
		attempts += 1
		time.sleep(1)

	# Error message if POST is unsuccessful
	if status >= 400:
		print("[ERROR] Could not send data after 5 attempts, please check \
			\nyour token credentials and internet connection")
		return False

	# Success message
	print("[INFO] request made properly, your device is updated")
	return True

if __name__ == '__main__':
	try:
		# Makes a POST request every 10 seconds
		while(True):
			# Message to be sent to ubidots
			msg = {'temp':temperature,'hum':humidity,'lum':luminosity}
			print("Sending data...")
			# Executes POST request
			post_request(msg)
			time.sleep(10)

	# Exit at CTRL + C
	except KeyboardInterrupt:
		print("END")
