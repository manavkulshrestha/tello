from djitellopy.tello import Tello
import cv2
import numpy as np
import threading

show = True

def show_camera(drone):
    if show:
        frame = drone.get_frame_read().frame
        cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        show = False

def main():
    drone = Tello()
    print('BATTERY', drone.get_battery())
    drone.connect()
    drone.streamon()

    drone.takeoff()

    threading.Thread(target=show_camera, args=(drone,)).start()

    drone.land()

if __name__ == "__main__":
    main()