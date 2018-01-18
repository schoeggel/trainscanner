import numpy as np
import cv2
from matplotlib import pyplot as plt
print(cv2.__version__)
#imgL = cv2.imread('img/13L.png',0)
#imgR = cv2.imread('img/13R.png',0)

# Features finden:
img = cv2.imread('img/13L.png', 0)

# Initiate STAR detector
orb = cv2.ORB_create(500, 1.2, 8, 30, 0, 2, 0, 31, 20)

# find the keypoints with ORB

# compute the descriptors with ORB
#kp, des = orb.compute(img, kp)


# draw only keypoints location,not size and orientation
img2=img
cv2.drawKeypoints(img,kp,img2,color=(0,255,0), flags=0)
#plt.imshow(img2),plt.show()
cv2.imshow("test", img2)
cv2.waitKey()
cv2.destroyAllWindows()

