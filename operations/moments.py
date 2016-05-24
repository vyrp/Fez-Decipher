import cv2
import numpy as np
import os
import re
import sys

from helpers import run_once
from matplotlib import pyplot as plt

_separator = re.compile(r"/|\\")


class Image():
    def __init__(self, filename, img, moment):
        self.filename = filename
        self.img = img
        self.moment = moment


def moments(foldername, opname, is_bw):
    foldername = _separator.split(foldername)[0]

    print "Starting [%s]" % opname

    # Calculating moments
    names = ["nu20", "nu11", "nu02", "nu30", "nu21", "nu12", "nu03"]
    images = []
    for filename in os.listdir(foldername):
        img = cv2.imread(os.path.join(foldername, filename), 0)
        moment = cv2.moments(img, is_bw)
        images.append(Image(filename, img, np.array([moment[name] for name in names])))

    L = min(7, len(images))  # noqa: constant
    for img1 in images:
        similars = sorted([((np.true_divide(img1.moment - img2.moment, img1.moment)**2).sum(), img2)
                           for img2 in images])

        plt.subplot(2, L, 1), plt.imshow(img1.img, cmap="gray")
        plt.title("Target: " + img1.filename), plt.xticks([]), plt.yticks([])

        for idx, elem in enumerate(similars[1:L+1]):
            plt.subplot(2, L, L + idx + 1), plt.imshow(elem[1].img, cmap="gray")
            plt.title("%s (%.2f)" % (elem[1].filename, elem[0])), plt.xticks([]), plt.yticks([])

        mng = plt.get_current_fig_manager()
        mng.window.state('zoomed')
        plt.show()

    print "Done"

moments.types = (str, str, bool)

if __name__ == "__main__":
    run_once(moments, sys.argv)
