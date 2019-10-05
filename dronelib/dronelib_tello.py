import socket
import threading
import time
from datetime import datetime
from math import atan2, cos, sin, degrees, radians, hypot, copysign
import cv2
from drone import Drone
from util import *


class Stats:
    def __init__(self, command, id):
        self.command = command
        self.response = None
        self.id = id

        self.start_time = datetime.now()
        self.end_time = None
        self.duration = None

    def add_response(self, response):
        self.response = response
        self.end_time = datetime.now()
        self.duration = self.get_duration()
        # self.print_stats()

    def get_duration(self):
        diff = self.end_time - self.start_time
        return diff.total_seconds()

    def print_stats(self):
        print '\nid: %s' % self.id
        print 'command: %s' % self.command
        print 'response: %s' % self.response
        print 'start time: %s' % self.start_time
        print 'end_time: %s' % self.end_time
        print 'duration: %s\n' % self.duration

    def got_response(self):
        if self.response is None:
            return False
        else:
            return True

    def return_stats(self):
        str = ''
        str += '\nid: %s\n' % self.id
        str += 'command: %s\n' % self.command
        str += 'response: %s\n' % self.response
        str += 'start time: %s\n' % self.start_time
        str += 'end_time: %s\n' % self.end_time
        str += 'duration: %s\n' % self.duration
        return str


class Tello:
    def __init__(self):
        self.local_ip = ''
        self.local_port = 8889
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # socket for sending cmd
        self.socket.bind((self.local_ip, self.local_port))

        # thread for receiving cmd ack
        self.receive_thread = threading.Thread(target=self._receive_thread)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        self.tello_ip = '192.168.10.1'
        self.tello_port = 8889
        self.tello_adderss = (self.tello_ip, self.tello_port)
        self.log = []

        self.MAX_TIME_OUT = 15.0
        self.local_video_ip = "0.0.0.0"
        self.local_video_port = 11111

    def send_command(self, command):
        """
        Send a command to the ip address. Will be blocked until
        the last command receives an 'OK'.
        If the command fails (either b/c time out or error),
        will try to resend the command
        :param command: (str) the command to send
        :param ip: (str) the ip of Tello
        :return: The latest command response
        """
        self.log.append(Stats(command, len(self.log)))

        self.socket.sendto(command.encode('utf-8'), self.tello_adderss)
        print 'sending command: %s to %s' % (command, self.tello_ip)

        start = time.time()
        while not self.log[-1].got_response():
            now = time.time()
            diff = now - start
            if diff > self.MAX_TIME_OUT:
                print 'Max timeout exceeded... command %s' % command
                # TODO: is timeout considered failure or next command still get executed
                # now, next one got executed
                return
        print 'Sent command: %s to %s' % (command, self.tello_ip)

    def _receive_thread(self):
        """Listen to responses from the Tello.

        Runs as a thread, sets self.response to whatever the Tello last returned.

        """
        while True:
            try:
                self.response, ip = self.socket.recvfrom(1024)
                print('from %s: %s' % (ip, self.response))

                self.log[-1].add_response(self.response)
            except socket.error, exc:
                print "Caught exception socket.error : %s" % exc

    def on_close(self):
        pass
        # for ip in self.tello_ip_list:
        #     self.socket.sendto('land'.encode('utf-8'), (ip, 8889))
        # self.socket.close()

    def get_log(self):
        return self.log

    def get_image(self):
        with new_suppress_stderr():
            video_capture = cv2.VideoCapture('udp://@0.0.0.0:' + str(self.local_video_port))
            if not video_capture.isOpened():
                video_capture.open('udp://@0.0.0.0:' + str(self.local_video_port))
            read_flag, frame = video_capture.read()
            return frame


class TelloDrone(Drone):

    def __init__(self):
        self.drone = Tello()
        self.height = 0.0
        self.yaw = 0.0
        self.x_cm = 0.0
        self.y_cm = 0.0
        self.z_cm = 0.0
        self.activated = False
        self.max_height = 500.0  # cm
        self.max_distance = 1000.0  # cm, max distance the drone is allowed to travel from start point in x or y direction

    def _turn(self, delta_yaw):
        delta_yaw %= 360

        if abs(delta_yaw) > 180:
            delta_yaw = (360 + delta_yaw) if (delta_yaw < 0) else (delta_yaw - 360)

        yaw_command = "ccw " if delta_yaw > 0 else "cw "
        if delta_yaw != 0:
            self.drone.send_command(yaw_command + str(abs(delta_yaw)))

        self.yaw += delta_yaw

    def _move_z_local_frame(self, cm):
        if (self.z_cm + cm >= self.max_height):
            err("Setpoint exceeding maximum allowed height. Aborting program")
            self.drone.send_command("stop")
            self.drone.send_command("land")
            sys.exit("Setpoint exceeded safety limits")

            return

        z_command = "up " if cm > 0 else "down "
        self.drone.send_command(z_command + str(abs(cm)))
        self.z_cm += cm

    def _move_x_local_frame(self, cm):
        dx = cos(radians(self.yaw)) * cm
        dy = sin(radians(self.yaw)) * cm

        if max(self.x_cm + dx, self.y_cm + dy) > self.max_distance:
            err("Setpoint exceeding maximum allowed distance from home. Aborting program.")
            self.drone.send_command("stop")
            self.drone.send_command("land")
            sys.exit("Setpoint exceeded safety limits")

        x_command = "forward " if cm > 0 else "back "
        self.drone.send_command(x_command + str(abs(cm)))

        self.x_cm += dx
        self.y_cm += dy

    def activate(self):
        self.drone.send_command("command")  # enable SDK mode
        self.drone.send_command("streamon")
        info("Activating drone...")
        # The video stream needs time to initialize
        time.sleep(3)
        self.activated = True
        info("Drone activated!")

    @property
    def position(self):
        return self.x_cm / 100, self.y_cm / 100, self.z_cm / 100

    def takeoff(self, height=0.8):  # height in m to match SimDrone
        if not self.activated:
            err("Could not take off. Drone is not yet activated.")
            return

        self.z_cm = 80  # Approximately default takeoff height
        self.drone.send_command("takeoff")
        self._move_z_local_frame(100 * height - self.z_cm)
        info("Takeoff complete")

    def land(self):
        if not self.activated:
            err("Could not land. Drone is not yet activated.")
            return

        info("Landing...")
        self.drone.send_command("land")

    def set_target(self, x, y, z=None, yaw=None):
        x_cm = x * 100
        y_cm = y * 100

        if z != None:
            z_cm = z * 100
            self._move_z_local_frame(z_cm - self.z_cm)

        dx = x_cm - self.x_cm
        dy = y_cm - self.y_cm

        target_direction = degrees(atan2(dy, dx))
        self._turn(target_direction - self.yaw)

        self._move_x_local_frame(hypot(dy, dx))

        if yaw != None:
            self._turn(yaw - self.yaw)

    @property
    def camera_image(self):
        image = self.drone.get_image()
        return image
