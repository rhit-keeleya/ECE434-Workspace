#!/usr/bin/env bash
# install.sh
# Date    2/17/2023
# Author  Abel Keeley
# 
# Install script for my Instruder Cam project. Details can be found here: https://github.com/rhit-keeleya/ECE434-Workspace/blob/master/project/README.md
# Will install necessary packages. This project was completed on a BeagleBone Black - which comes preconfigured with software. As a result, this script may 
# not be comprehensive, and some required packages may have been overlooked or excluded.

sudo apt update
# nginx-based webserver used for remote review of footage
sudo apt install nginx -y
# necessary utilities
sudo apt install apache2-utils -y
# php used for indexing/manipulating footage on the webserver
sudo apt install php8.1-fpm -y
sudo apt install php-fpm -y
# motion is used to actually run the camera, trigger scripts and save footage upon motion detection
sudo apt install motion -y

echo "WARNING: this project uses NGROK to allow for remote access. As this cannot easily be installed automatically, you should install it manually here: https://ngrok.com/download "
