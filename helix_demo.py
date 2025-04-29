from src.drone import Drone
from djitellopy.tello import Tello
import numpy as np
import time


def main():
    do_drone = True

    if do_drone:
        drone = Tello()
        drone.connect()
        print(drone.get_battery())

        drone.takeoff()

    radius = 60
    stretch = 5
    n_rotations = 1

    prev_x, prev_y, prev_z = radius, 0, 0
    
    for i in range(n_rotations):
        for t in np.linspace(0, 2 * np.pi, 15)[1:]:
            x, y, z = radius * np.cos(t), radius * np.sin(t), stretch * t
            dx, dy, dz = x - prev_x, y - prev_y, z - prev_z
            cmd = round(dy), round(-dx), round(dz)
            print(f' {dy} {-dx} {dz} -> {cmd}')


            if do_drone:
                cmd = (cmd[0], cmd[1], 10)                
                drone.go_xyz_speed(*cmd, 100)
            # print(round(dy), round(-dx), round(dz))
            # print((dy), (-dx), (dz))s
            # print(dx, dy, dz)
            prev_x, prev_y, prev_z = x, y, z
            
            time.sleep(0.1)

    if do_drone:
        drone.land()


if __name__ == "__main__":
    main()