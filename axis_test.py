from djitellopy.tello import Tello

drone = Tello()
drone.connect()

drone.takeoff()

# drone.go_xyz_speed(20, 0, 0, 10) #F
# drone.go_xyz_speed(0, 20, 0, 10) #L
# drone.go_xyz_speed(0, 0, 20, 10) #U

drone.land()
