import numpy as np
import cv2
from matplotlib import pyplot as plt
print(cv2.__version__)
#imgL = cv2.imread('img/13L.png',0)
#imgR = cv2.imread('img/13R.png',0)

# Features finden:
f= "img/karton.jpg"
f= "img/13L.png"
img = cv2.imread(f,0)
imc = cv2.imread(f,0)

corners = cv2.goodFeaturesToTrack(img, 7, 0.05, 25)
corners = cv2.goodFeaturesToTrack(img, 50, 0.05, 25)
corners = np.float32(corners)

for item in corners:
    x, y = item[0]
   # cv2.circle(img, (x,y), 5, 255, -1)
   # cv2.circle(imc, (x,y), 25, [0, 50, 255, 128], 15, 1)
    cv2.circle(imc, (x,y), 25, [200,150,0], 15, 1)


imc= cv2.resize(imc, (1500,800))
cv2.imshow("Top 'k' features", imc)
cv2.waitKey()
cv2.destroyAllWindows()
