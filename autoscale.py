import requests
import base64
import json

from apscheduler.schedulers.blocking import BlockingScheduler

from config import APP, KEY, PROCESS

# Generate Base64 encoded API Key
BASEKEY = base64.b64encode(":" + KEY)
# Create headers for API call
HEADERS = {
    "Accept": "application/vnd.heroku+json; version=3",
    "Authorization": BASEKEY
}


def scale(size):
    payload = {'quantity': size}
    json_payload = json.dumps(payload)
    url = "https://api.heroku.com/apps/" + APP + "/formation/" + PROCESS
    try:
        result = requests.patch(url, headers=HEADERS, data=json_payload)
    except:
        print ("test!")
        return None
    if result.status_code == 200:
        return "Success!"
    else:
        return "Failure"


@sched.scheduled_job('interval', minutes=1)
def job():
    print ('Scaling ...')
    print (scale(0))


sched.start()
