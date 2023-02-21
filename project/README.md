# Intruder Cam

A motion activated intruder detection and alert system. For a general overview see the [elinux](https://elinux.org/ECE434_Project_-_Intruder_Cam) page. Requires a computer running Linux (I used a BeagleBone Black, but there are many alternatives) and a camera.

## Install
As this was made on a BeagleBone Black, some software was already preinstalled (like python) and I will not go into detail as to how to install it (as far better guides are already readily available). The included install.sh script should download most of the needed software, but I will go ahead and list the requirements here as well.

* [Motion](https://motion-project.github.io/) - for motion detection
* [Python](https://www.python.org/) - for miscellaneous scripting
* [ngrok](https://dashboard.ngrok.com/get-started/setup) - for setting up a remote tunnel
* [Nginx](https://docs.nginx.com/nginx/admin-guide/installing-nginx/installing-nginx-open-source/) - for hosting basic webserver
* [PHP-FPM](https://www.digitalocean.com/community/tutorials/php-fpm-nginx) - for more interactive webpages

## Setup
As you'll likely want to customize this a bit, I'll just provide my configuration files and detail any notable settings. Note that all the python files should be in the same directory, and that both execute.sh and index.php should be placed in the root folder of the webserver.

##### Motion
See motion.conf. You'll need to point the motion service to this config file on startup.

```
# Start in daemon (background) mode and release terminal.
daemon off
```
I found that using daemon mode led to permission issues when configuring Motion to automatically launch as a service. Your mileage may very, but I would suggest leaving it off to begin with.
```
# Target directory for pictures, snapshots and movies
target_dir /tmp/motion/footage
```
I'd suggest making this directory somewhere in /tmp/ to prevent your hard drive getting filled up with videos/pictures you may not wish to save. You will be able to manually save footage via the webserver, if you see something you want to archive.
```
# Video device (e.g. /dev/video0) to be used for capturing.
videodevice /dev/video0
```
As I only had one camera, I used video0 - this may be different for your setup.
```
# Command to be executed when a movie file is closed.
on_movie_end '/home/debian/ECE434-Workspace/project/notify_event.py /temporary/%Y-%m-%d/ >> /tmp/err.log 2>&1'
```
This is where the magic happens. You'll want to change this to point to the location of the notify_event.py script on your machine. Note that the output of the script (both stdout and stderr) is being redirected to /tmp/err.log - quite helpful for debugging any errors!
```
# Container/Codec to used for the movie. See motion_guide.html
movie_codec mp4
```
I find mp4 files tend to be playable directly from a browser - no download required!
```
# File name(without extension) for movies relative to target directory
movie_filename %Y-%m-%d/event%v-%T
```
Saves files to a directory corresponding to the date. If you change this be sure to update the parameters in the "on_movie_end" command to match!

##### Nginx
See included footage folder for full config. You'll need to place this config file in `/etc/nginx/sites-available/`.
```
listen 8000;
listen [::]:8000;
```
Tell Nginx to listen for connections on port 8000 - purely an abitrary choice of port number.
```
root /var/www/footage/html;
index index.php index.html index.htm index.nginx-debian.html;
```
Specifies both the root directory of the webserver and what files can be considered valid indexes. Note that index.php is included as a valid index. Both execute.sh and index.php should be placed in whatever directory is specified here. A symbolic link called `temporary` should be created in the root directory pointing to whatever target directory motion is storing its footage in.
```
auth_basic "My Footage";
auth_basic_user_file /etc/apache2/.htpasswd;
```
User authentication - optional but suggested. You can generate htpasswd files by installing apache2-utils and executing `htpasswd -c /etc/apache2/.htpasswd userNameToAdd`.
```
location ~ \.php$ {
	    include snippets/fastcgi-php.conf;	
	    fastcgi_pass unix:/var/run/php/php7.4-fpm.sock;
	    include fastcgi_params;
	}
```
Tells the webserver how to handle .php files - i.e. they should be executed on the server-side rather than just served to the client.
### ngrok
This [page](https://dashboard.ngrok.com/get-started/setup) should walk you through most of the setup. After you are done, you should edit your ~/.config/ngrok/ngrok.yml file to open up whatever port the Nginx server is listening to. I've included my ngrok.yml as an example, using port 8000.
### Automatically launching the services
Using systemctl, you can automatically start ngrok, nginx, php-fpm, and motion on startup. Nginx and php-fpm should already be configured as part of their install process, so running `systemctl enable <service name>` for nginx.service, php7.4-fpm.service, phpsessionclean.service, and phpsessionclean.timer should work. For ngrok and motion you'll need to add the corresponding .service file to `/lib/systemd/system/`. Note that for ngrok you'll need to modify
```
ExecStart=/usr/local/bin/ngrok "service" "run" "--config" "/home/debian/.config/ngrok/ngrok.yml"
```
to point to the location of your edited ngrok.yml file. Similarly for motion, modify
```
ExecStart=/usr/bin/motion -c /home/debian/ECE434-Workspace/project/motion.conf
```
to point to the location of motion.conf on your machine.
After doing so, you should be able to enable them as well.
### IFTTT Notifications
After making an [IFTTT](https://ifttt.com/explore) account, simply create a new applet. Select webhooks -> web request as the "If This", and notifications -> rich notifications from IFTTT app as the "Then That". Set the rich notification link to be `{{Value1}}`. Visit [this page](https://maker.ifttt.com/use/) and select documentation. This page should show your unique key - copy it to a file named `IFTTT.key` in the same directory as the notify_event.py script. Lastly, replace 
```
event = "motion_event_started"
```
in fire_notification.py with the name of the web request you setup for the "If This" event.
### Logging to Google Sheets
Follow [this](https://developers.google.com/sheets/api/quickstart/python) quick guide to enable the sheets api. Then in sheets.py modify
```
SAMPLE_SPREADSHEET_ID = '1HYiyoPwh7UqmKjXuOukN3I2lU7gyDsUY33D4qIqe7uU'
SAMPLE_RANGE_NAME = 'A2'
PATH = '/home/debian/ECE434-Workspace/project/'
```
the ID to match whatever sheet you want to log data to, and the path to match the location of the file.

## Timeline
|Milestone|Description|Target Date|Completed?|
|-|-|-|-|
|1|By M1, the camera system should be able to reliably alert the user if motion is detected.| N/A | Yes|
|2|By M2, the camera system should be able to generate a link that the user can follow to a webserver capable of serving images/video of any motion events captured.|2/6/23| Yes|
|3|By M3, the camera system should be able allow the user to remotely select whether to save any videos or pictures permanently (as of now, they are written to /tmp/ and would be lost if the system is powercycled). | 2/13/23| No|
|4|By M4, the camera system should be complete, including a nice UI. | 2/20/23| No|
