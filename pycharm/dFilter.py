import cv2
import statistics
import numpy
from itertools  import compress

def dFilter(matches, kp1, kp2, tolerancepixeldist=1):
    # Nach der mFilter Anwendung bleiben noch solche FalsePositive Matches,
    # die auf dem richtigen Winkel liegen, aber viel zu weit vom auseinander liegen
    # nach Pixelkoordinaten Bild1/Bild2. àhnlich wie im mFilter wird nur eine begrenzte
    # Abweichung vom median-Distanz toleriert. Img-Dimesnion 4096x3000

    # Initialize lists
    list_kp1 = []
    list_kp2 = []
    list_d = []

    # For each match...
    for mat in matches:
        # Get the matching keypoints for each of the images
        img1_idx = mat.queryIdx
        img2_idx = mat.trainIdx

        # x - columns
        # y - rows
        # Get the coordinates
        (x1, y1) = kp1[img1_idx].pt
        (x2, y2) = kp2[img2_idx].pt

        # Append to each list
        list_kp1.append((x1, y1))
        list_kp2.append((x2, y2))
        list_d.append( ( (y2-y1)**2 + (x2-x1)**2)**0.5)

    referenzDistanz = statistics.median(list_d)
    print("referenzDistanz  =  " + str(referenzDistanz))

    # Maske erstellen anhand der Maske die Matches filtern
    maske = [(abs(referenzDistanz-x) < tolerancepixeldist) for x in list_d]
    newmatches = compress(matches, maske)
    newmatches = list(newmatches)   # geht sonst nach einem zugriff verloren
    dfilterinfo = "dFilter: before/after (tolerance=" + str(tolerancepixeldist)
    dfilterinfo += "px): " + str(newmatches.__len__()) + " / " + str(matches.__len__())
    print(dfilterinfo)

    if 0 == 1:
        import matplotlib.pyplot as plt
        plt.hist(list_d, bins='auto')  # arguments are passed to np.histogram
        plt.title("Histogram with 'auto' bins")
        plt.show()

    return newmatches, dfilterinfo


