import os
import cv2
import configparser
from timeit import default_timer as timer
import util
import mFilter
import matplotlib.pyplot as plt
from random import shuffle


standardfile = 'tmp/cfg-test-2017-12-0100000001.ini'

def cvprocess(img1, img2, inifile = standardfile, imgoutpath = None, seiteLRS="undefined"):
    # Verarbeitet eine .ini Datei und führt die Verarbeitungskette durch
    # gemäss den in der .ini Datei definierten Parametern. Return=Resultate ausser Bild
    # Das Bild selber wird (falls angegeben) in den Ordner 'imgoutpath' gespeichert.
    # inifile: Datei im .ini format mit den Prozessparamtern
    # img1, img2: Die Bilder als Graustufenbilder (bereits geladen)
    # imgoutpath: None = Das verarbeitete Bildpaar mit den Matches wird angezeigt aber nicht gespeichert
    #             pfad = Das verarbeitete Bildpaar wird gespeichert. Ganze Ausführung im Hintergrund
    #
    timerstart = timer()

    # outputpath - Argument prüfen:
    if imgoutpath is None:
        background = False
        print("opencv Version: " + cv2.__version__)
    else:
        imgoutpath = str(imgoutpath)
        if os.path.isdir(imgoutpath):
            background = True
        else:
            raise Exception("Path '" + imgoutpath + "' is not an existing directory.")

    # INI Datei laden
    ini = configparser.ConfigParser()
    ini.read(inifile)

    # todo: falls detector = descriptor ist: verwenden von detectAndCompute function, weil schneller


# DETECTOR
    cfg = ini['detector']
    c = util.IniTypehandler(cfg)
    detectortype = cfg['type'].lower()
    if detectortype == "brisk":
        if not background:
            print("using", detectortype)
        detect = cv2.BRISK_create(c.get('threshold'),
                                  c.get('octaves'),
                                  c.get('scale'))

    elif detectortype == "orb":
        if not background:
            print("using", detectortype)
        detect = cv2.ORB_create(c.get('maxfeatures'),
                                c.get('scale'),
                                c.get('levels'),
                                edgeThreshold=25,
                                WTA_K=c.get('orb_wtak'))

    elif detectortype == "surf":
        if not background:
            print("using", detectortype)
        detect = cv2.xfeatures2d_SURF.create(c.get('threshold'),
                                             c.get('octaves'),
                                             c.get('octaveLayers'),
                                             c.get('extended'),
                                             c.get('upright'))

    elif detectortype == "goodfeaturestotrack":
        if not background:
            print("using", detectortype)
            # todo: implement
            print("unfertig")

    else:
        errmsg = "Unknown algorithm '" + detectortype + "'."
        if not background:
            print(errmsg)
        raise Exception(errmsg)

    # find keypoints:
    kp1 = detect.detect(img1)
    kp2 = detect.detect(img2)
    foundkp1 = len(kp1)
    foundkp2 = len(kp2)


# DESCRIPTOR
    cfg = ini['extractor']
    c = util.IniTypehandler(cfg)
    detectortype = cfg['type'].lower()
    if detectortype == "brisk":
        if not background:
            print("using", detectortype)
        describe = cv2.BRISK_create(c.get('threshold'),
                                  c.get('octaves'),
                                  c.get('scale'))


    #dummie:
    describe = cv2.xfeatures2d.FREAK_create()

    # descriptors
    kp1, des1 = describe.compute(img1, kp1)
    kp2, des2 = describe.compute(img2, kp2)

    # MATCHER
    # create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match descriptors.
    matches = bf.match(des1, des2)

    # Geht nur wenn sequentiell verglichen wird: Filtern nach Parallelität der Matches
    if seiteLRS == "L" or seiteLRS == "R":
        matches = sorted(matches, key=lambda x: x.distance)
        newmatches, mfilterinfo = mFilter.mFilter(matches, kp1, kp2, 0.1)
    else:
        newmatches = None
        mfilterinfo = "no mFilter"

    # zufällige n Matches einzeichnen.
    n = 75
    shuffle(matches)
    # img4 = cv2.drawMatches(img1, kp1, img2, kp2, matches[:n], None, flags=2)
    # plt.imshow(img4), plt.show()

    if newmatches:
        shuffle(newmatches)
        img5 = cv2.drawMatches(img1, kp1, img2, kp2, newmatches[:n], None, flags=2)
        # plt.imshow(img5), plt.show()
    else:
        img5 = cv2.drawMatches(img1, kp1, img2, kp2, matches[:n], None, flags=2)

    if imgoutpath is not None:
        cfg = ini['file']
        dst = imgoutpath + cfg['name'] + ".jpg"
        print("writing image to file:")
        print(dst)
        util.writeLQjpg(img5, dst, inifile, [mfilterinfo])

    # todo: Dummie Return ersetzen
    timerend = timer()
    return {"Errors" : None, "Result": "ok", "TimeElapsed": timerend-timerstart}



