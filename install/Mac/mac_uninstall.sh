#!/bin/sh
echo 'Uninstalling the Tello Video Stream module'

echo 'You might need to enter your password'

brew update

sudo pip uninstall matplotlib -y
sudo pip uninstall numpy -y
sudo pip install pillow -y
sudo pip install opencv-python -y
sudo pip uninstall pip -y

brew uninstall tcl-tk
brew uninstall ffmpeg
brew uninstall boost-python
brew uninstall boost

echo 'Uninstallation Done!'
