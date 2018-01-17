import cv2
import statistics
import numpy
from itertools  import compress



def mFilter(matches, kp1, kp2, toleranceDegrees=1):
    # entfernt alle matches, deren verbindungslinien zu stark vom Medianwinkel abweichen
    # Precondition: Matches müssen zwingend sortiert sein
    # Damit es mit L+R wie auch mit Einseitig sequentiell geschossenen Bildern funktioniert,
    # werden die Winkel der Linien berechnet, wie sie auch in den Anzeige dargestellt werden,
    # wenn beide Bilder nebeneinander liegen. Img-Dimesnion 4096x3000

    # Initialize lists
    list_kp1 = []
    list_kp2 = []
    list_m = []

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
        list_m.append((y2-y1)/(x2-x1+4097))

    winkel = numpy.arctan(list_m)
    winkel = numpy.rad2deg(winkel)

    #Von den obersten 10% der Matches den median-Winkel ermitteln
    topten = winkel[:int(winkel.__len__() / 10)]
    referenzWinkel = statistics.median(topten)
    # print(*topten, sep='\n')
    print("referenzWinkel  =  " + str(referenzWinkel))

    # Maske erstellen anhand der Maske die Matches filtern
    maske = [(abs(referenzWinkel-x) < toleranceDegrees) for x in winkel]
    newmatches = compress(matches, maske)
    newmatches = list(newmatches)   # geht sonst nach einem zugriff verloren
    mfilterinfo = "Anzahl gefilterte / ungefilterte Matches mit Toleranz " + str(toleranceDegrees) + "°: "
    mfilterinfo += str(newmatches.__len__()) + " / " + str(matches.__len__())
    print(mfilterinfo)

    if 0 == 1:
        import matplotlib.pyplot as plt
        plt.hist(winkel, bins='auto')  # arguments are passed to np.histogram
        plt.title("Histogram with 'auto' bins")
        plt.show()

    return newmatches, mfilterinfo


