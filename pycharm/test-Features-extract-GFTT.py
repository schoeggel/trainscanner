import numpy as np
import cv2
from matplotlib import pyplot as plt
print(cv2.__version__)

# Features finden:
# f = "img/karton.jpg"
f = "img/13L.png"
img = cv2.imread(f, 0)
imc = cv2.imread(f)

gftt = cv2.GFTTDetector_create()



imc = cv2.resize(imc, (1500, 800))
dmode = 'GoodFeaturesToTrack GFTT'
imc = cv2.putText(imc, 'feature detection mode: ' + dmode, (100,100), 1, 3, (255,255,255),3)
cv2.imshow('feature detection mode: ' + dmode, imc)
cv2.imwrite('out/' + dmode + '.jpg', imc)
cv2.waitKey()
cv2.destroyAllWindows()
