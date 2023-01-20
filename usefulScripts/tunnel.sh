#!/bin/bash

echo "Forwarding localhost:3000 to debian@$1..."
#takes beagleboard IP as argument $1
ssh -p2022 -L 127.0.0.1:3000:localhost:3000 debian@$1
