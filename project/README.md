# Intruder Cam

A motion activated intruder detection and alert system. For a general overview see the (elinux)[https://elinux.org/ECE434_Project_-_Intruder_Cam] page. Requires a computer running Linux (I used a BeagleBone Black, but there are many alternatives) and a camera.

## Install
As this was made on a BeagleBone Black, some software was already preinstalled (like python) and I will not go into detail as to how to install it (as far better guides are already readily available). The included install.sh script should download most of the needed software, but I will go ahead and list the requirements here as well.

* (Motion)[https://motion-project.github.io/] - for motion detection
* (Python)[https://www.python.org/] - for miscellaneous scripting
* (ngrok)[https://dashboard.ngrok.com/get-started/setup] - for setting up a remote tunnel
* (Nginx)[https://docs.nginx.com/nginx/admin-guide/installing-nginx/installing-nginx-open-source/] - for hosting basic webserver
* (PHP-FPM)[https://www.digitalocean.com/community/tutorials/php-fpm-nginx] - for more interactive webpages

## Setup
As you'll likely want to customize this a bit, I'll just provide my configuration files and detail any notable settings.

### Motion
See motion.conf.

># Start in daemon (background) mode and release terminal.
>daemon off
I found that using daemon mode led to permission issues when configuring Motion to automatically launch as a service. Your mileage may very, but I would suggest leaving it off to begin with.

># Target directory for pictures, snapshots and movies
>target_dir /tmp/motion/footage
I'd suggest making this directory somewhere in /tmp/ to prevent your hard drive getting filled up with videos/pictures you may not wish to save. You will be able to manually save footage via the webserver, if you see something you want to archive.

># Video device (e.g. /dev/video0) to be used for capturing.
>videodevice /dev/video0
As I only had one camera, I used video0 - this may be different for your setup.

># Command to be executed when a movie file is closed.
>on_movie_end '/home/debian/ECE434-Workspace/project/notify_event.py /temporary/%Y-%m-%d/ >> /tmp/err.log 2>&1'
This is where the magic happens. You'll want to change this to point to the location of the notify_event.py script on your machine. Note that the output of the script (both stdout and stderr) is being redirected to /tmp/err.log - quite helpful for debugging any errors!

># Container/Codec to used for the movie. See motion_guide.html
>movie_codec mp4
I find mp4 files tend to be playable directly from a browser - no download required!

># File name(without extension) for movies relative to target directory
>movie_filename %Y-%m-%d/event%v-%T
Saves files to a directory corresponding to the date. If you change this be sure to update the parameters in the "on_movie_end" command to match!

### Nginx & PHP

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
