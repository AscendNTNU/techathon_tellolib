#!/bin/sh

echo 'Installing the Tello Video Stream module'
echo 'You might need to enter your password'

sudo apt-get update -y

# install python 2.7
sudo apt-get install python2.7 python-pip -y
sudo pip install --upgrade pip

#switch to python2.7
sudo update-alternatives --install /usr/bin/python python /usr/bin/python2 150 
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 100

sudo apt-get update -y

# install dependencies
sudo apt-get install libboost-all-dev -y
sudo apt-get install libavcodec-dev -y
sudo apt-get install libswscale-dev -y
sudo apt-get install python-numpy -y
sudo apt-get install python-matplotlib -y
sudo pip install opencv-python
sudo apt-get install python-imaging-tk

echo 'Installation Done!'
