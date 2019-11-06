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


def web_scale(size):
    payload = {'quantity': size}
    json_payload = json.dumps(payload)
    url = "https://api.heroku.com/apps/" + APP + "/formation/" + PROCESS
    try:
        result = requests.patch(url, headers=HEADERS, data=json_payload)
    except:  # noqa
        print("Error ocurred in scaling")
        return None
    if result.status_code == 200:
        return "Success in scaling!"
    else:
        return "Failure in scaling"


def worker_scale(size):
    payload = {'quantity': size}
    json_payload = json.dumps(payload)
    url = "https://api.heroku.com/apps/" + APP + "/formation/" + PROCESS_WORKER
    try:
        result = requests.patch(url, headers=HEADERS, data=json_payload)
    except:  # noqa
        print("Error ocurred in scaling")
        return None
    if result.status_code == 200:
        return "Success in scaling!"
    else:
        return "Failure in scaling"


@sched.scheduled_job('interval', minutes=1)
def scale_down():
    """Scale web app to 0 and scale worker to 1"""
    print('Scaling Web app down...')
    print(web_scale(0))
    print(worker_scale(1))


@sched.scheduled_job('interval', minutes=2)
def scale_up():
    print('Scaling Web app up...')
    print(web_scale(1))
    print(worker_scale(0))


sched.start()
