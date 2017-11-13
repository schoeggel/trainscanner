import numpy as np
import cv2
from matplotlib import pyplot as plt
print(cv2.__version__)
#imgL = cv2.imread('img/13L.png',0)
#imgR = cv2.imread('img/13R.png',0)

# Features finden:
img = cv2.imread("img/clouds.jpg",0)
cv2.imshow("test", img)
cv2.waitKey()

