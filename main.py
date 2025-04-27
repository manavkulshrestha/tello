from djitellopy.tello import Tello
import time
from src.drone import Drone

# drone = Tello()
# drone.connect()
# drone.takeoff()
# # drone.go_xyz_speed(0, 20, 0, 10)
# time.sleep(2)
# drone.land()

drone = Drone(ip='10.164.8.208', port=5000, verbose=True)

drone.takeoff()
drone.land()