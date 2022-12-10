#!/usr/bin/env bash

# setupNetworking.sh	12/10/2022	keeleya
# Configures a number of quality-of-life and security settings. Sets hostnameto BeagleBone2751,
# updates ssh port to 2022, sets up IPtables to reject any connections to port 3000 except from
# localhost (use portforwarding!), and enables the IDE server hosted on port 3000.

# Update Hostname
sudo hostnamectl set-hostname BeagleBone2751
# Update hosts file to match new name
sudo sed -i '/^127.0.1.1*/ c\127.0.1.1 BeagleBone2751.localdomain BeagleBone2751' /etc/hosts
echo Set hostname to BeagleBone2751...

# Update ssh port
sudo sed -i '/^#Port 22/ c\Port 2022' /etc/ssh/sshd_config
echo Set ssh to port 2022...

# Install IPtables
sudo apt-get -y install iptables
# IPtables configuration 
sudo iptables -A INPUT -p tcp --dport 3000 -s localhost -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 3000 -j DROP
# Save IPtables rules
sudo iptables-save
echo Setup iptables to only allow connections to port 3000 that are forwarded through localhost...

# Enable IDE
sudo systemctl enable bb-code-server.service
echo Enabled the IDE hosted on port 3000...
