#!/usr/bin/env python3

import fire_notification
import sheets

# send notification
key = fire_notification.get_key()
success = fire_notification.motion_event(key)

# log time/success status
sheets.append_values([success])