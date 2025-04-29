from src.drone import Drone
from djitellopy.tello import Tello
import numpy as np
import time


def main():
    do_drone = True

    if do_drone:
        drone = Tello()
        drone.connect()
        print('BATTERY', drone.get_battery())

        drone.takeoff()

    n_sides = 3
    side_len = 80
    prev_x, prev_y, prev_z = side_len, 0, 0
    n_times = 3

    for n in range(n_times):
        for i in range(1, n_sides+1):
            theta = i * 2*np.pi/n_sides
            x, y = side_len * np.cos(theta), side_len * np.sin(theta)
            dx, dy = x - prev_x, y - prev_y

            cmd = round(dy), round(-dx), 10
            print(f' {dy} {-dx} {10} -> {cmd}')
            if do_drone:
                drone.go_xyz_speed(*cmd, 100)
                time.sleep(0.1)
                drone.flip('f')
            prev_x, prev_y = x, y
    
    if do_drone:
        drone.land()


if __name__ == "__main__":
    main()