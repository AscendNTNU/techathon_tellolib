## TelloDrone class documentation

### Usage
Add the following to the top of your code, assuming you have placed your file in the root directory of this repository:
```python
from dronelib.dronelib_tello import TelloDrone
```

The TelloDrone uses a right handed coordinate system, with x forward, y to the left and z up.

All distances are in meters. Yaw is in degrees, where counterclockwise rotation is positive.

### Initialization
Initialization takes no arguments, and can be done like this:
```python
drone = TelloDrone()
```

### Methods and properties

```python 
TelloDrone.activate()
```
This needs to be called after creating a new TelloDrone object, and will prepare the drone for flight and
video transfer.

---

```python
TelloDrone.takeoff(z=0.8)
``` 

Takes off to the specified height. Default is 0.8 meters.

---
```python
TelloDrone.land()
```
Lands the drone.

---
```python
TelloDrone.set_target(x,y,z=None, yaw=None)
```

Turns the drone towards the target, and flies there in a straight line. If no z value is provided,
the drone will keep its current height. If no yaw value is provided, the drone will keep
the direction it faced when moving to the target.

Setpoints less than 20cm away from the drone will be ignored. This is a limitation in the Tello firmware.


---
```python
TelloDrone.camera_image
```
A numpy ndarray object of the current camera frame.
The image can be saved by passing it to the method `save_image(frame)` in `dronelib.utils`.

---
```python
TelloDrone.position
```
A tuple containing the (x,y,z) coordinates of the drone

---
```python
TelloDrone.yaw
```
The current yaw of the drone in degrees. Positive values are counterclockwise.


