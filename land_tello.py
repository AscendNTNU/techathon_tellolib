from dronelib_tello import TelloDrone

def main():
    drone = TelloDrone()
    drone.activate()
    drone.drone.send_command("land")

if __name__ == "__main__":
        main()