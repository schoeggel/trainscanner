# der feeder füttert den cvprocessor mit .ini filennamen und mit Bilddaten
# TODO: Automatisieren, damit ganze Batchs verarbeitet werden
# TODO: Parallelisieren
# pool = multiprocessing.Semaphore(multiprocessing.cpu_count())  etc..
# ini list in gleiche stücke hacken: scipy chunks

import cv2
import cvprocesssor

# Bilder laden (Ein Bild nur einmal laden für alle .ini Files)
bildnr = "./../sbbimg/21"
seiteLRS = "S"  # Links / Rechts / Stereo

if seiteLRS == "S":
    imc1 = cv2.imread(bildnr + "L.png")
    img1 = cv2.cvtColor(imc1, cv2.COLOR_BGR2GRAY)
    imc2 = cv2.imread(bildnr + "R.png")
    img2 = cv2.cvtColor(imc2, cv2.COLOR_BGR2GRAY)
else:
    imc1 = cv2.imread(str(int(bildnr) - 1) + seiteLRS + ".png")
    img1 = cv2.cvtColor(imc1, cv2.COLOR_BGR2GRAY)
    imc2 = cv2.imread(bildnr + seiteLRS + ".png")
    img2 = cv2.cvtColor(imc2, cv2.COLOR_BGR2GRAY)

try:
    results = cvprocesssor.cvprocess(img1,
                                     img2,
                                     'cfg/process/processtest2.ini', 'tmp/', seiteLRS, bildnr)
except Exception as detail:
    print(detail)
    results = ('ERROR', str(detail))


print('----------')
print('Results:')
print((results))
