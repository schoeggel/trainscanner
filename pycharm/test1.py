import numpy as np
import cv2
from matplotlib import pyplot as plt
print(cv2.__version__)
#imgL = cv2.imread('img/13L.png',0)
#imgR = cv2.imread('img/13R.png',0)

# Features finden:
img = cv2.imread('img/13L.png', 0)

# Initiate STAR detector
orb = cv2.ORB_create()

# find the keypoints with ORB
kp = orb.detect(img, None)

# compute the descriptors with ORB
kp, des = orb.compute(img, kp)

img2 = img
# draw only keypoints location,not size and orientation
cv2.drawKeypoints(img, kp, img ,color=(128, 0, 0), flags=0)
cv2.imshow("key", img), cv2.waitKey()
#plt.imshow(img2), plt.show()