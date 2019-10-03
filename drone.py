from abc import ABCMeta, abstractmethod, abstractproperty

class Drone:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def activate(self):
        pass

    @abstractmethod
    def takeoff(self, height):
        pass

    @abstractmethod
    def set_target(self,x,y,z,yaw):
        pass

    @abstractproperty
    def camera_image(self):
        pass

    @abstractproperty
    def yaw(self):
        pass

    @abstractproperty
    def position(self):
        pass
