from djitellopy.tello import Tello
import cv2
import numpy as np

drone = Tello()
drone.connect()
print(drone.get_battery())

# drone.takeoff()
drone.streamon()

frames = []
for i in range(100):
    frame = drone.get_frame_read().frame
    frames.append(frame)
    print(f'got frame {i}')

print(frame.shape)
np.savez('cap.npz', frames=np.array(frames))

# cv2.imshow('Frame', frame)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# print(frame)

