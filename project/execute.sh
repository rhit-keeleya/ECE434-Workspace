#!/usr/bin/env bash

echo "Executing $1 on $2"

OLD_PATH="$2/"

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
    if [ -d $NEW_PATH ]
    then
        # directory is already archived?
        echo "Error: Directory $NEW_PATH already has files!" 
    else
        echo "Removing all files in $OLD_PATH, transfered to $NEW_PATH"
        # make sure the new path is empty
        rm -rf $NEW_PATH
        # do the move
        mkdir -p `dirname $NEW_PATH`
        mv $OLD_PATH $NEW_PATH
    fi
    # # want to copy folder /temporary/arbitary/path/ to /permanent/arbitary/path/
    # NEW_PATH=`echo $OLD_PATH | sed "s/temporary/permanent/"`
    # echo "Copying from $OLD_PATH to $NEW_PATH"
    # # move first
    # mv  $OLD_PATH $NEW_PATH
    # # copy back to original location
    # cp -r $NEW_PATH $OLD_PATH
elif [ $1 = "Delete" ]
then
        if [ ! -d $OLD_PATH ]
    then
        # directory to delete doesn't exist
        echo "Error: Directory $OLD_PATH is already EMPTY!" 
    else
        NEW_PATH=`echo $OLD_PATH | sed "s/permanent/temporary/"`
        echo "Removing all files in $OLD_PATH, transfered to $NEW_PATH"
        # make sure the new path is empty
        rm -rf $NEW_PATH
        # do the move
        mkdir -p `dirname $NEW_PATH`
        mv $OLD_PATH $NEW_PATH
    fi
    # # want to move folder /permanent/arbitary/path/ to /temporary/arbitary/path/
    # NEW_PATH=`echo $OLD_PATH | sed "s/permanent/temporary/"`
    # echo "Moving from $OLD_PATH to $NEW_PATH"
    # # do the move
    # mv $OLD_PATH $NEW_PATH
else
    echo "Error: Unknown action!" >&2
fi