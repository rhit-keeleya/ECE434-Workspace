Various project related files stored here. Not sure quite yet what it is gonna look like...

# Timeline
|Milestone|Description|Target Date|Completed?|
|-|-|-|-|
|1|By M1, the camera system should be able to reliably alert the user if motion is detected.| N/A | Yes|
|2|By M2, the camera system should be able to generate a link that the user can follow to a webserver capable of serving images/video of any motion events captured.|2/6/23| Yes|
|3|By M3, the camera system should be able allow the user to remotely select whether to save any videos or pictures permanently (as of now, they are written to /tmp/ and would be lost if the system is powercycled). | 2/13/23| No|
|4|By M4, the camera system should be complete, including a nice UI. | 2/20/23| No|

# Ideas:

Store pics/videos in tmp, serve them on webserver - send URL to owner on motion detect. Maybe fire up an ngrok tunnel, and send the link to the owner to allow remote access? SHould that be automatic, or something the owner "requests" or otherwise triggers?

Allow user to "save" media -> transfer out of tmp. 

Periodically check storage used... if almost full, purge oldest tmp files to free up room?

# Things being done
    
    Logging debugging stuff to google sheets
    Using nginx as webserver on port 8000
    Using ngrok service to make tunnel, and IFTTT to serve notifications w/ link on motion detection.
    Have to have motion running as www-data, so can properly move directories around.
