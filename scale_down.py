import requests
import base64
import json

from apscheduler.schedulers.blocking import BlockingScheduler

from config import APP, KEY, PROCESS, PROCESS_WORKER
sched = BlockingScheduler()

# Generate Base64 encoded API Key
BASEKEY = base64.b64encode(KEY.encode())

# Create headers for API call
HEADERS = {
    "Accept": "application/vnd.heroku+json; version=3",
    "Authorization": BASEKEY
}

# Scale down the web app
web_size = 0
result = None

payload = {'quantity': web_size}
json_payload = json.dumps(payload)
url = "https://api.heroku.com/apps/" + APP + "/formation/" + PROCESS
try:
    result = requests.patch(url, headers=HEADERS, data=json_payload)
except:  # noqa
    print("Error ocurred in scaling down web app")
if result.status_code == 200:
    print("Success in scaling down web app!")
else:
    print("Failure in scaling down web app!")

# Then scale up the worker
worker_size = 1
result = None

payload = {'quantity': worker_size}
json_payload = json.dumps(payload)
url = "https://api.heroku.com/apps/" + APP + "/formation/" + PROCESS_WORKER
try:
    result = requests.patch(url, headers=HEADERS, data=json_payload)
except:  # noqa
    print("Error ocurred in scaling up worker")
if result.status_code == 200:
    print("Success in scaling up worker!")
else:
    print("Failure in scaling up worker")
