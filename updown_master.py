from djitellopy.tello import Tello
import time
from src.drone import Drone

# drone = Tello()
# drone.connect()
# drone.takeoff()
# # drone.go_xyz_speed(0, 20, 0, 10)
# time.sleep(2)
# drone.land()

rdrone = Drone(ip='10.164.8.208', port=5000, verbose=True)
ldrone = Tello()
ldrone.connect()
print(ldrone.get_battery())

SPEED, OFFT = 100, 40

drones = [rdrone, ldrone]

for drone in drones:
    drone.takeoff()
    drone.go_xyz_speed(0, 0, 60, SPEED)

drones[0].go_xyz_speed(0, 0, OFFT, SPEED)

time.sleep(3)
print('starting updown')
sgn = 1
for _ in range(6):
    drones[0].go_xyz_speed(0, 0, -sgn*OFFT, SPEED)
    drones[1].go_xyz_speed(0, 0, sgn*OFFT, SPEED)

    sgn = -sgn

for drone in drones:
    drone.land()

print('Done')
time.sleep(10)