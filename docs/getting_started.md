# Getting started

This document will describe how to install the dependencies and run the _tellolib_ demo.

## Installation

### Linux (Tested on Ubuntu 18.04)
Go to the "install/Linux" folder using the command line, and run:
```shell script
chmod +x linux_install.sh
./linux_install.sh
```

### Mac
Go to the "install/Mac" folder using the command line, and run:
```shell script
chmod a+x ./mac_install.sh
./mac_install.sh
```

### Windows
We recommend using Windows Subsystem for Linux (WSL) to install Ubuntu 18.04 inside Windows 10
 and run the project from there.
Please refer to the [official Microsoft guide](https://docs.microsoft.com/en-us/windows/wsl/install-win10)
 for installation instructions, and then follow our Linux installation instructions from inside the subsystem.

If you do not want to install the subsystem and feel comfortable with installing packages manually, 
the required packages can be found in the mac and linux installation scripts.


## Running the project
- __Step 1:__ Turn on the Tello and connect your computer to its WiFi network. 
Each Tello has its own network, and will be marked with an identifier. 
Please do not connect to Tello networks other than your own.
- __Step 2:__ Open the project folder using the terminal, and run:
```shell script
python2 tello_demo.py
```
- __Step 3:__ Turn off the Tello when the program has finished to conserve battery.

You may use _tello_demo.py_ as a reference for your own competition code. \
_Tellolib_ has a similar same interface to the _dronelib_ library for the simulator 
challenge, so please refer to its documentation.

