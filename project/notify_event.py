#!/usr/bin/env python3

import requests
import os

os.getenv('IFTTT_KEY')

key = os.getenv('IFTTT_KEY')
event = "motion_event_started"

payload = {"value1":"hello", "value2":" from the", "value3":" beagle!"}
url = "https://maker.ifttt.com/trigger/"+event+"/with/key/"+key

r = requests.post(url, stream=True, data=payload)
print(r.text)