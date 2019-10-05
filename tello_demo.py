from dronelib.dronelib_tello import TelloDrone
from dronelib.util import *
from time import sleep

def main():
    drone = TelloDrone()
    drone.activate()

    drone.takeoff()

    drone.set_target(1,0)

    print(drone.position)
    print(drone.yaw)

    drone.set_target(0,0)

    print(drone.position)
    print(drone.yaw)

    image = drone.camera_image
    save_image(image)

    drone.land()



if __name__ == "__main__":
        main()
