# der feeder füttert den cvprocessor mit .ini filennamen und mit Bilddaten
# TODO: Automatisieren, damit ganze Batchs verarbeitet werden
# TODO: Parallelisieren
# pool = multiprocessing.Semaphore(multiprocessing.cpu_count())  etc..
# ini list in gleiche stücke hacken: scipy chunks

import cv2
import cvprocesssor
import os
import numpy as np
from multiprocessing.dummy import Pool as ThreadPool



# BATCH CONFIGURATION:
bildnr = "13"
bildfolder = "img/"         # Verzeichnis mit den Zugbildern
seiteLRS = "L"              # Links / Rechts / Stereo
inifolder = "cfg/ini/"      # Verzeichnis mit alle .ini Files
outputfolder = "tmp/"       # Verzeichnis für match-jpg und csv
threads = 1                     # Anzahl Thrads


def feedsingle(inifile):
    print("feeder gestartet.")
    # Lässt den cvprocessor mit einer angebenen ini durchlaufen
    results = ''
    try:
        results = cvprocesssor.cvprocess(img1,
                                         img2,
                                         inifile, outputfolder, seiteLRS, bildnr)
        os.rename(inifile, inifile + ".ok")

    except Exception as detail:
        print(detail)
        results = ('ERROR', str(detail))
        os.rename(inifile, inifile + ".err")

    finally:
        print('----------')
        print('Results:')
        print(results)



# Prüfe ob das Zeilverzeichnis keine jpg oder csv dateien enthält
foundsmth = False
for f in os.listdir(outputfolder):
    if f.endswith(".csv") or f.endswith(".jpg"):
        foundsmth = True
if foundsmth:
    input("Achtung! Zielverzeichnis enthält jpg oder csv Dateien. Weiter nach Tastendruck.")


# Bilder nur genau einmal laden
if seiteLRS == "S":
    imc1 = cv2.imread(bildfolder + bildnr + "L.png")
    img1 = cv2.cvtColor(imc1, cv2.COLOR_BGR2GRAY)
    imc2 = cv2.imread(bildfolder + bildnr + "R.png")
    img2 = cv2.cvtColor(imc2, cv2.COLOR_BGR2GRAY)
else:
    imc1 = cv2.imread(bildfolder + str(int(bildnr) - 1) + seiteLRS + ".png")
    img1 = cv2.cvtColor(imc1, cv2.COLOR_BGR2GRAY)
    imc2 = cv2.imread(bildfolder + bildnr + seiteLRS + ".png")
    img2 = cv2.cvtColor(imc2, cv2.COLOR_BGR2GRAY)


# inifilelist erstellen
allinifiles = []
for f in os.listdir(inifolder):
    if f.endswith(".ini"):
        #print(os.path.join("/mydir", file))
        allinifiles.append(os.path.join(inifolder, f))

print("found ini:")
print(allinifiles)


# nicht mehr benötigt #Die iniliste auf anzahl cpu splitten
# chunks = np.array_split(allinifiles, threads)


# make the Pool of workers
pool = ThreadPool(threads)

# process in own threads
results = pool.map(feedsingle, allinifiles)

# close the pool and wait for the work to finish
pool.close()
pool.join()


