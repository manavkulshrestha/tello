import cv2
from djitellopy import Tello

tello = Tello()
tello.connect()
print(tello.get_battery())

tello.streamon()
frame_read = tello.get_frame_read()

tello.takeoff()
cv2.imwrite("picture.png", frame_read.frame[:, :, ::-1])

tello.land()