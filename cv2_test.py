import numpy as np
import cv2

vid = np.load('cap.npz')['frames']
print(vid.shape)

cv2.imshow('Image', vid[-1])
cv2.waitKey(0)
cv2.destroyAllWindows()