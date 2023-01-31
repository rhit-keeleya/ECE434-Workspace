Various project related files stored here. Not sure quite yet what it is gonna look like...


Ideas:

Store pics/videos in tmp, serve them on webserver - send URL to owner on motion detect. Maybe fire up an ngrok tunnel, and send the link to the owner to allow remote access? SHould that be automatic, or something the owner "requests" or otherwise triggers?

Allow user to "save" media -> transfer out of tmp. 

Periodically check storage used... if almost full, purge oldest tmp files to free up room?

Debugging:
Exported IFTTT key, does that env variable hang around after reboot?


Use Apache2 webserver

    edit /etc/apache2/sites-available/footage.conf

    password file @ /etc/apache2/.htpasswd
    
    serves the contents of /var/www/footage/