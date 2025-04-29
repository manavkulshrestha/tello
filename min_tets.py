from djitellopy.tello import Tello

drone = Tello()
drone.connect()
print(drone.get_battery())

drone.takeoff()

drone.go_xyz_speed(19, 1, 2, 10)

drone.land()