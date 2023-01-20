#!/usr/bin/env bash
## timeWaster.sh	Abel Keeley	1/19/22
## Runs an infinite loop that prints stuff out.

INDEX=0

while [ true ]
do
	echo -ne "Echoed: $INDEX times..."\\r
	let INDEX=$INDEX+1
done
