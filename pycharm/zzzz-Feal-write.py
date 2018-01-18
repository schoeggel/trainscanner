import numpy as np
import cv2
import util



from matplotlib import pyplot as plt
print(cv2.__version__)
#imgL = cv2.imread('img/13L.png',0)
#imgR = cv2.imread('img/13R.png',0)

# Features finden:
img = cv2.imread("img/13R.png",0)
#cv2.imshow("test", img)
#cv2.waitKey()

name = 'tmp/jpgtestA-util.jpg'
txt = 'Das ist ein Test für den Header-Overlay-Text im JPG lowquality Bild das irgendwo gespeichert werden soll.'
moretext = ['blaaaa', 'Line2', 'parameter Test: 1.22355434534', 'Type=This is not a type', 'Summary: now we are done.']

util.writeLQjpg(img, name, 'Kopftext', moretext)
