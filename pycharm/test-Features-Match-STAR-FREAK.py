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

detect = cv2.xfeatures2d.StarDetector_create()
describe = cv2.xfeatures2d.FREAK_create()

# find the keypoints
kp1 = detect.detect(img1)
kp2 = detect.detect(img2)

# Text Info / create filename
dmode = 'STAR-FREAK-hamming2'
info = "-"
foundkp1 = len(kp1)
foundkp2 = len(kp2)


# and descriptors
kp1, des1 = describe.compute(img1, kp1)
kp2, des2 = describe.compute(img2, kp2)


# create BFMatcher object
bf = cv2.BFMatcher(cv2.NORM_HAMMING2, crossCheck= True)  #wirft error wenn SURF detector kombiniert mit
#bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)

# Match descriptors.
matches = bf.match(des1, des2)

# Sort them in the order of their distance.
matches = sorted(matches, key=lambda x: x.distance)

img3 = img1
# Draw first n matches.
n = 500
img4 = cv2.drawMatches(img1, kp1, img2, kp2, matches[:n], None, flags=2)

#for item in kp1:
#    x, y = item.pt
#    cv2.circle(img4, (int(x), int(y)), 16, (0, 255, 0), 2, 1)

zoom = 0.2


img4 = cv2.putText(img4, 'detect/compute: ' + dmode, (40, 80), 1, 6, (0, 0, 255),3)
img4 = cv2.putText(img4, 'Keypoints:' + str((foundkp1,foundkp2)), (40, 160), 1, 6, (0, 0, 255), 3)
img4 = cv2.putText(img4, 'matches Limit: ' + str(n), (40, 240), 1, 6, (0, 0, 255), 3)
img4 = cv2.putText(img4, 'misc: ' + info, (40, 320), 1, 6, (0, 0, 255), 3)

cv2.imwrite('out/' + dmode + '.jpg', img4)
img4 = cv2.resize(img4, (int(zoom*2*4096), int(zoom*3000))) #4096x3000 original grösse pro Bild
cv2.imshow('mode: ' + dmode, img4)

cv2.waitKey()
cv2.destroyAllWindows()
