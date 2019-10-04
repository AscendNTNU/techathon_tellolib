from dronelib_tello import TelloDrone
from util import *
from time import sleep

def main():
    drone = TelloDrone()
    drone.activate()
    drone.takeoff()
    drone.set_target(1,0)
    drone.set_target(11,0)
    drone.set_target(0,0)
    drone.set_target(0,20)
    #image = drone.camera_image()
    #save_image(image)

    drone.drone.send_command("land")



if __name__ == "__main__":
        main()