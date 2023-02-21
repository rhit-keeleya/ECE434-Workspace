#!/usr/bin/env python3

import requests
import os

def motion_event(key, link):
    event = "motion_event_started"
    
    print(link)

    payload = {"value1":link, "value2":" from the", "value3":" beagle!"}
    url = "https://maker.ifttt.com/trigger/"+event+"/with/key/"+key

    r = requests.post(url, stream=True, data=payload)
    if "Congratulations!" in r.text:
        return True
    return False


def get_key():
    # assumes that the key is stored in this file
    file = open("/home/debian/ECE434-Workspace/project/IFTTT.key")
    key = file.read()
    return key


if __name__ == '__main__':
    #executed as script
    key = get_key()
    print(motion_event(key, 'www.google.com'))
