import cv2

print(cv2.__version__)

# Features finden:
#f = "img/karton.jpg"
f = "img/13L.png"
img = cv2.imread(f, 0)
imc = cv2.imread(f)


bp = cv2.SimpleBlobDetector_Params()
blob = cv2.SimpleBlobDetector_create()
freakExtractor = cv2.xfeatures2d.FREAK_create()


keypoints1 = blob.detect(img)
descriptors = freakExtractor.compute(img, keypoints1)


for item in keypoints1:
    x, y = item.pt
    cv2.circle(imc, (int(x), int(y)), 16, (0, 255, 0), 2, 1)


imc = cv2.resize(imc, (1500, 800))
dmode = 'BLOB'
imc = cv2.putText(imc, 'feature detection mode: ' + dmode, (100,100), 1, 3, (255,255,255),3)
cv2.imshow('feature detection mode: ' + dmode, imc)
cv2.imwrite('out/' + dmode + '.jpg', imc)
cv2.waitKey()
cv2.destroyAllWindows()
