from dronelib_tello import TelloDrone
from time import sleep

def main():
    drone = TelloDrone()
    drone.activate()

    drone.takeoff(1)
    sleep(2)
    drone.set_target(1,0)
    sleep(2)
    drone.set_target(0,0)
    drone.drone.send_command("land")


if __name__ == "__main__":
        main()