import numpy as np
import cv2
from matplotlib import pyplot as plt
print(cv2.__version__)

# Features finden:
# f = "img/karton.jpg"
f = "img/13L.png"
img = cv2.imread(f, 0)
imc = cv2.imread(f)

corners = cv2.goodFeaturesToTrack(img, 1000, 0.05, 25)
corners = np.float32(corners)

#cv2.cvtColor(img,cv2.COLOR_GRAY2BGR,imc)
for item in corners:
    x, y = item[0]
    # cv2.circle(img, (x,y), 5, 255, -1)
    # cv2.circle(imc, (x,y), 25, [0, 50, 255, 128], 15, 1)
    cv2.circle(imc, (x, y), 25, (0, 255, 0), 15, 1)


imc = cv2.resize(imc, (1500, 800))
dmode = 'GoodFeaturesToTrack'
imc = cv2.putText(imc, 'feature detection mode: ' + dmode, (100,100), 1, 3, (255,255,255),3)
cv2.imshow('feature detection mode: ' + dmode, imc)
cv2.imwrite('out/' + dmode + '.jpg', imc)
cv2.waitKey()
cv2.destroyAllWindows()
