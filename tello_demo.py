from dronelib.dronelib_tello import TelloDrone
from dronelib.util import *
from time import sleep

def main():
    drone = TelloDrone()
    drone.activate()
    drone.takeoff()
    image = drone.camera_image()
    save_image(image)

    drone.land()



if __name__ == "__main__":
        main()
