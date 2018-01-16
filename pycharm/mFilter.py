import cv2
import statistics
import numpy



def mFilter(matches, kp1, kp2, toleranceDegrees=5):
    # entfernt alle matches, deren verbindungslinien zu stark vom Medianwinkel abweichen
    # Precondition: Matches müssen zwingend sortiert sein

    # Initialize lists
    list_kp1 = []
    list_kp2 = []
    list_m   = []

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
        list_m.append((y2-y1)/(x2-1))


    list_m = numpy.arctan(list_m)
    m = statistics.median(list_m)
    tolerance = toleranceDegrees / 180 * numpy.pi

    list_m = [x for x in list_m if abs(m-x) < (tolerance)]

# todo aus der bereinigten list_m die matches entsprechend filtern.

    if 0 == 1:
        import matplotlib.pyplot as plt
        plt.hist(list_m, bins='auto')  # arguments are passed to np.histogram
        plt.title("Histogram with 'auto' bins")
        plt.show()

    return matches


