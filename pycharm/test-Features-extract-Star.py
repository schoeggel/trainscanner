import numpy as np
import cv2


from matplotlib import pyplot as plt
print(cv2.__version__)

# Features finden:
f = "img/karton.jpg"
f = "img/13L.png"
img = cv2.imread(f, 0)
imc = cv2.imread(f)

star = cv2.xfeatures2d.StarDetector_create()
#surf = cv2.xfeatures2d.SURF_create()
freakExtractor = cv2.xfeatures2d.FREAK_create()

keypoints1 = star.detect(img)
descriptors = freakExtractor.compute(img, keypoints1)

for item in keypoints1:
    x, y = item.pt
    cv2.circle(imc, (int(x), int(y)), 16, (0, 255, 0), 2, 1)


imc = cv2.resize(imc, (1500, 800))
cv2.imshow("Top 'k' features", imc)
cv2.waitKey()
cv2.destroyAllWindows()
