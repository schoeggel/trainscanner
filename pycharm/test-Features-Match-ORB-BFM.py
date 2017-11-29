import numpy as np
import cv2


from matplotlib import pyplot as plt
print(cv2.__version__)

# Bilder laden
bildnr = "13"

imc1 = cv2.imread("img/" + bildnr + "L.png")
img1 = cv2.cvtColor(imc1, cv2.COLOR_BGR2GRAY)
imc2 = cv2.imread("img/" + bildnr + "R.png")
img2 = cv2.cvtColor(imc2, cv2.COLOR_BGR2GRAY)

detect = cv2.ORB_create()

# find the keypoints
kp1 = detect.detect(img1, None)
kp2 = detect.detect(img2, None)

# and descriptors
kp1, des1 = detect.compute(img1, kp1)
kp2, des2 = detect.compute(img2, kp2)



# create BFMatcher object
bf = cv2.BFMatcher(cv2.NORM_HAMMING2, crossCheck=True)

# Match descriptors.
matches = bf.match(des1, des2)

# Sort them in the order of their distance.
matches = sorted(matches, key=lambda x: x.distance)

img3=img1
# Draw first n matches.
n = 50
img4 = cv2.drawMatches(img1, kp1, img2, kp2, matches[:n], None, flags=2)

#for item in keypoints1:
#    x, y = item.pt
#    cv2.circle(imc1, (int(x), int(y)), 16, (0, 255, 0), 2, 1)

zoom = 0.2

imc1 = cv2.resize(img4, (int(zoom*2*4096), int(zoom*3000))) #4096x3000 original grösse pro Bild
dmode = 'Match ORB'
imc1 = cv2.putText(imc1, 'detect + match: ' + dmode, (5, 15), 1, 1, (0, 0, 255), 1)
cv2.imshow('feature detection mode: ' + dmode, imc1)
#cv2.imwrite('out/' + dmode + '.jpg', imc1)

cv2.waitKey()
cv2.destroyAllWindows()
