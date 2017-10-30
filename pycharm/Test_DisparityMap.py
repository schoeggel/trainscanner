import numpy as np
import cv2
from matplotlib import pyplot as plt
print(cv2.__version__)
imgL = cv2.imread('img/13L.png',0)
imgR = cv2.imread('img/13R.png',0)
stereo = cv2.StereoSGBM_create(numDisparities=16, blockSize=10)
# stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
disparity = stereo.compute(imgL,imgR)
plt.imshow(disparity)
plt.show()
cv2.imshow("disp", disparity), cv2.waitKey()