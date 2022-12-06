#!/bin/bash

# firewall.sh <- configures firewall to block remote access to port 3000
# Still allows ssh tunneling though...
# Author: keeleya

if `sudo nft list table inet filter | grep -q "ip saddr 127.0.0.1 tcp dport 3000 accept"`; then
	echo Rules already found, exitting...
else
	echo Rules not found, setting up
	# whitelist localhost traffic
	sudo nft add rule inet filter input ip saddr 127.0.0.1 tcp dport 3000 accept
	# drop all other traffic to port 3000
	sudo nft add rule inet filter input tcp dport 3000 drop
fi
