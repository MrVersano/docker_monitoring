# Docker Monitoring
This scripts monitors the existing Docker containers using the Docker REST API and alerts to Slack if any container is not running.


## Installation

### Enable Docker REST API 
```bash
vim /lib/systemd/system/docker.service
```

Find a line that looks like this: `ExecStart=/usr/bin/dockerd` and add the following to it (if it doesn't already exist):
```bash
-H=tcp://0.0.0.0:5555
```
This will add the Docker REST API on port 5555. Save and close the file.

### Restart the daemon and service
```bash
sudo systemctl daemon-reload
sudo service docker restart
```

## Usage
1. Configure the *post_to_slack* function with our Slack credentials. I use an environemnt variable for the Slack token and I suggest doing the same.
2. Configure the variables *server* and *port* to the address and port of your docker host
3. Run the script using:
```bash
python3 docker_monitoring.py
```
I suggest using Cron to have this script run periodically to check on the containers.