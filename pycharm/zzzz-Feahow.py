import numpy as np
import cv2



from matplotlib import pyplot as plt
print(cv2.__version__)
#imgL = cv2.imread('img/13L.png',0)
#imgR = cv2.imread('img/13R.png',0)

# Features finden:
img = cv2.imread("img/13L.png",0)
#cv2.imshow("test", img)
#cv2.waitKey()

imgc = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)


name = 'tmp/jpgtestA-'
txt = 'Das ist ein Test für den Header-Overlay-Text im JPG lowquality Bild das irgendwo gespeichert werden soll.'
moretext = ['blaaaa', 'Line2', 'parameter Test: 1.22355434534', 'Type=This is not a type', 'Summary: now we are done.']
moretextStart = 160
headerColor = (128, 0, 255)
textColor = (255, 0, 255)


for q in [10]:
    im = cv2.putText(imgc, str(q).zfill(3) + txt, (40, 80), 1, 6, headerColor, 3)
    for line in moretext:
        im = cv2.putText(im, line, (40, moretextStart), 1, 6, textColor, 3)
        moretextStart += 80

    cv2.imwrite(name+str(q).zfill(3)+'.jpg', im, [cv2.IMWRITE_JPEG_QUALITY, q])
