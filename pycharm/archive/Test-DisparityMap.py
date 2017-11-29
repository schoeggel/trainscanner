import numpy as np
import cv2
from matplotlib import pyplot as plt

print(cv2.__version__)
imgL = cv2.imread('img/13L.png', 0)
imgR = cv2.imread('img/13R.png', 0)
#imgL = cv2.imread('img/im0.png', 0)
#imgR = cv2.imread('img/im1.png', 0)


stereo = cv2.StereoSGBM_create(minDisparity=0, numDisparities=128, blockSize=9, uniquenessRatio=2,speckleWindowSize=50, speckleRange=2)
# stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
disparity = stereo.compute(imgL, imgR)
plt.imshow(disparity, "gray")
plt.show()
#cv2.imshow("disp", disparity), cv2.waitKey()
