#!/usr/bin/env bash

echo "Executing $1 on $2"

OLD_PATH=$2

# handle edge case where /tmp/ directory structure doesn't yet exist...
# should only occur when testing.

if [ ! -d ./temporary ]
then
    TEMP=/tmp/motion/footage
    echo "Warning: ./temporary doesn't yet exist, creating directory $TEMP"
    mkdir -p $TEMP
fi

if [ $1 = "Archive" ]
then
    NEW_PATH=`echo $OLD_PATH | sed "s/temporary/permanent/"`
    echo Old path: $OLD_PATH
    echo New path: $NEW_PATH
    mkdir -p `dirname $NEW_PATH`
    mv $OLD_PATH $NEW_PATH
elif [ $1 = "Delete" ]
then
    if [ ! -d `dirname $OLD_PATH` ]
    then
        # directory to delete doesn't exist
        echo "Error: Directory `dirname $OLD_PATH` is already EMPTY!" 
    else
        NEW_PATH=`echo $OLD_PATH | sed "s/permanent/temporary/"`
        echo "Removing all files in $OLD_PATH, transfered to temp space @ $NEW_PATH"
        mkdir -p `dirname $NEW_PATH`
        mv $OLD_PATH $NEW_PATH
    fi
else
    echo "Error: Unknown action!" >&2
fi