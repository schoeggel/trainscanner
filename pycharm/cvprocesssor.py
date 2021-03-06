import os
import cv2
import numpy as np
import configparser
from timeit import default_timer as timer
import util
import mFilter
import dFilter
import calibMatrix
import matplotlib.pyplot as plt
from random import shuffle
import reproFilter
import calibMatrix


cal = calibMatrix.CalibData()  # Alle Matrizen laden: F, intrins., extr.
standardfile = 'tmp/cfg-test-2017-12-0100000001.ini'

def drawlines(img1,img2,lines,pts1,pts2):
    """ img1 - image on which we draw the epilines for the points in img2
        lines - corresponding epilines
        source: https://docs.opencv.org/3.2.0/da/de9/tutorial_py_epipolar_geometry.html"""
    r, c = img1.shape
    img1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)
    img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
    for r, pt1, pt2 in zip(lines, pts1, pts2):
        color = tuple(np.random.randint(0, 255, 3).tolist())
        x0, y0 = map(int, [0, -r[2] / r[1]])
        x1, y1 = map(int, [c, -(r[2] + r[0] * c) / r[1]])
        img1 = cv2.line(img1, (x0, y0), (x1, y1), color, 1)
        img1 = cv2.circle(img1, tuple(pt1), 5, color, -1)
        img2 = cv2.circle(img2, tuple(pt2), 5, color, -1)
    return img1, img2


def cvprocess(img1, img2, inifile = standardfile, imgoutpath=None, seiteLRS="undefined", bildnr="undefined"):
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

    try:
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

        elif detectortype == "star":
            if not background:
                print("using", detectortype)
            detect = cv2.xfeatures2d_StarDetector.create(c.get('scale'),                    # maxSize
                                                         c.get('threshold'),                # responseThreshold
                                                         10,                                # default
                                                         8,                                 # default
                                                         c.get('fast_nonmaxSuppression'))   # suppressNonmaxSize


        elif detectortype == "fast":
            if not background:
                print("using", detectortype)
            detect = cv2.FastFeatureDetector_create(c.get('threshold'),
                                                    c.get('fast_nonmaxSuppression'),
                                                    c.get('scale'))    # scale für Type 0,1,2

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

        if detectortype == "orb":
            if not background:
                print("using", detectortype)
            describe = cv2.ORB_create(c.get('maxfeatures'),
                                      c.get('scale'),
                                      c.get('levels'),
                                      edgeThreshold=25,
                                      WTA_K=c.get('orb_wtak'))

        if detectortype == "latch":
            if not background:
                print("using", detectortype)
            describe = cv2.xfeatures2d.LATCH_create()

        if detectortype == "freak":
            if not background:
                print("using", detectortype)
            describe = cv2.xfeatures2d_FREAK.create(patternScale=c.get('scale'),
                                                    nOctaves=c.get('octaves'))

        # descriptors
        kp1, des1 = describe.compute(img1, kp1)
        kp2, des2 = describe.compute(img2, kp2)

        # MATCHER
        # create BFMatcher object
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        # Match descriptors.
        matches = bf.match(des1, des2)
        matches = sorted(matches, key=lambda x: x.distance)

        # Geht nur wenn sequentiell verglichen wird: Filtern nach Parallelität der Matches
        if seiteLRS == "L" or seiteLRS == "R":
            mfiltermatches, mfilterinfo = mFilter.mFilter(matches, kp1, kp2, 0.1)
            dfiltermatches, dfilterinfo = dFilter.dFilter(mfiltermatches, kp1, kp2, 25)

        # Die Bilder sind zum selben Zeitpunkt aufgenommen von L und von R:
        elif seiteLRS == "S":
            cfg = ini['Filter']
            c = util.IniTypehandler(cfg)
            pts1 = []
            pts2 = []
            good = matches[:c.get('maxMatches')]
            for match in good:
                pts2.append(kp2[match.trainIdx].pt)
                pts1.append(kp1[match.queryIdx].pt)



            cfg = ini['3d']
            c = util.IniTypehandler(cfg)
            pts1 = np.int32(pts1)
            pts2 = np.int32(pts2)
            F_ransac, mask = cv2.findFundamentalMat(pts1, pts2, cv2.FM_LMEDS)
            F_calibration = cal.f   # todo: .ini getrieben F laden oder ermitteln, errorMaxDistance ebenfalls via .ini
            if c.get('MatrixF').lower() == "ransac":
                F = F_ransac
            else:
                F = F_calibration

            c = util.IniTypehandler(ini['Filter'])
            dfiltermatches, dfilterinfo = reproFilter.filterReprojectionError(good, F, c.get('reproMaxDistance'), pts1, pts2)
            mfiltermatches = dfiltermatches
            mfilterinfo = "bfmatcher matches: " + str(matches.__len__())


        # zufällige n Matches einzeichnen.
        n = 75
        shuffle(matches)
        # img4 = cv2.drawMatches(img1, kp1, img2, kp2, matches[:n], None, flags=2)
        # plt.imshow(img4), plt.show()

        if dfiltermatches:
            shuffle(dfiltermatches)
            img5 = cv2.drawMatches(img1, kp1, img2, kp2, dfiltermatches[:n], None, flags=2)
            #plt.imshow(img5), plt.show()
        else:
            img5 = cv2.drawMatches(img1, kp1, img2, kp2, matches[:n], None, flags=2)


# TRIANGULATION
# Punkte müssen im 2xN Format sein und float: l = np.array([[ 304],[ 277]],dtype=np.float)
# https://stackoverflow.com/questions/46163831/output-3d-points-change-everytime-in-triangulatepoints-using-in-python-2-7-with
        pts1 = np.array(pts1.transpose(), dtype=np.float)
        pts2 = np.array(pts2.transpose(), dtype=np.float)
        test = cv2.triangulatePoints(cal.pl, cal.pr, pts1, pts2)
        print("Triangulation result:", test.shape)
        fn = "tmp/3dpoints002"
        test = test[:-1] / test[-1]  # https://pythonpath.wordpress.com/import-cv2/
        # test = test / np.max(test)
        np.save(fn + ".npy", test.T)
        np.savetxt(fn + ".asc", test.T, "%10.8f")


        if imgoutpath is not None:
            cfg = ini['file']
            dst = imgoutpath + cfg['name']
            print("writing image to file:")
            print(dst + ".jpg")
            headertext = inifile + ': ' + ini['detector']['type'] + '/' + ini['extractor']['type']
            util.writeLQjpg(img5, dst + ".jpg", headertext, [mfilterinfo, dfilterinfo, "img:" + bildnr])

    except Exception as detail:
        if imgoutpath is not None:
            # Irgendein Fehler in der Verarbeitung, will aber trotdem das csv schreiben!
            cfg = ini['file']
            dst = imgoutpath + cfg['name']
            util.writeCSV(dst + ".csv", bildnr, seiteLRS, ini, 'error', 'error', detail, -1)
        raise

    if imgoutpath is not None:
        # benötigte Anagaben: bildnr, seiteLRS[L|R|S], config, detectortype, descriptortype, totalmatches, filteredmatches
        util.writeCSV(dst + ".csv",
                      bildnr,
                      seiteLRS,
                      ini,
                      str(matches.__len__()),
                      str(mfiltermatches.__len__()),
                      str(dfiltermatches.__len__()),
                      timer()-timerstart)

    timerend = timer()
    return {"Errors": None, "Result": "ok", "TimeElapsed": timerend-timerstart}



"""
        # Find epilines corresponding to points in right image (second image) and
        # drawing its lines on left image
        lines1 = cv2.computeCorrespondEpilines(pts2.reshape(-1, 1, 2), 2, F)
        lines1 = lines1.reshape(-1, 3)
        img10, img11 = drawlines(img1, img2, lines1, pts1, pts2)

        # Find epilines corresponding to points in left image (first image) and
        # drawing its lines on right image
        lines2 = cv2.computeCorrespondEpilines(pts1.reshape(-1, 1, 2), 1, F)
        lines2 = lines2.reshape(-1, 3)
        img8, img9 = drawlines(img2, img1, lines2, pts2, pts1)
        plt.subplot(121), plt.imshow(img10)
        plt.subplot(122), plt.imshow(img8)
        plt.show()
"""
