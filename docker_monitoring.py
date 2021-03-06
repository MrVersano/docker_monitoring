import json
import requests
import os

# Funciton to send a notification to a slack channel
def post_to_slack(channel_name, message):
	
	# slack access bot token
	slack_token = os.environ['aerith']

	data = {
		'token': slack_token,
		'channel': channel_name,
		'as_user': True,
		'text': message,
        'link_names': True
	}

	requests.post(url='https://slack.com/api/chat.postMessage', data=data)

# Configure server and port
server = 'localhost'
port = 5555

# Pull a list of all containers from the Docker API
r = requests.get(url=f'http://{server}:{port}/containers/json?all=1')
containers_data = r.json()

stopped_containers = []

# Loop through containers to see if a container is not running
for container in containers_data:
    if container['State'] != 'running':
        stopped_containers.append(container['Names'][0].replace("/", ""))

# Post message to slack if any container is not running
if len(stopped_containers) > 0:
    post_to_slack('ms-alerts', f'@here Docker Alert!\nThe following containers have stopped running on the reporting server: {stopped_containers}')
