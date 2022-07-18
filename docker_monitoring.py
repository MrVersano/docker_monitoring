import json
import requests
import os
import docker
import socket



# Load Config File
with open('/etc/ms_config/reports_config.json') as config_file:
	config = json.load(config_file)

# Funciton to send a notification to a slack channel
def post_to_slack(channel_name, message):
	
	# slack access bot token
	slack_token = config['aerith']

	data = {
		'token': slack_token,
		'channel': channel_name,
		'as_user': True,
		'text': message,
		'link_names': True
	}

	requests.post(url='https://slack.com/api/chat.postMessage', data=data)


not_running_containers = [] # A list of containers that are not running
client = docker.from_env()
for container in client.containers.list():
	if container.status != 'running':
		not_running_containers.append(container.name)

if len(not_running_containers) == 0:
	print("All containers running.")
else:
	for container in not_running_containers:
		post_to_slack("es_alert_errors", f"WARNING: Container {container} is not running on server {socket.gethostname()}")

