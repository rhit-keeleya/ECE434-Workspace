#!/usr/bin/env python3

import fire_notification
import build_link
import sheets
import sys

# build link
folder = sys.argv[1]
folder = "/?b="+folder.replace('/', '%2F')
# /?b=permanent%2F2023-02-14%2Fevent01
link = build_link.get_tunnel()+folder

# send notification
key = fire_notification.get_key()
success = fire_notification.motion_event(key, link)

# log time/success status
sheets.append_values([success,link])
