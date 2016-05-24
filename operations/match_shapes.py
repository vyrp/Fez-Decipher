import cv2
import os
import re
import sys

from helpers import run_once
from matplotlib import pyplot as plt

_separator = re.compile(r"/|\\")


class Image():
    def __init__(self, filename, img):
        self.filename = filename
        self.img = img


def match_shapes(foldername, opname, method):
    foldername = _separator.split(foldername)[0]

    print "Starting [%s]" % opname

    # Loading images
    images = []
    for filename in os.listdir(foldername):
        img = cv2.imread(os.path.join(foldername, filename), 0)
        images.append(Image(filename, img))

    L = min(7, len(images))  # noqa: constant
    for img1 in images:
        similars = sorted([(cv2.matchShapes(img1.img, img2.img, method, 0), img2)
                           for img2 in images])

        plt.subplot(2, L, (L+1)/2), plt.imshow(img1.img, cmap="gray")
        plt.title("Target: " + img1.filename), plt.xticks([]), plt.yticks([])

        for idx, elem in enumerate(similars[1:L+1]):
            plt.subplot(2, L, L + idx + 1), plt.imshow(elem[1].img, cmap="gray")
            plt.title("%s (%.2e)" % (elem[1].filename, elem[0])), plt.xticks([]), plt.yticks([])

        mng = plt.get_current_fig_manager()
        mng.window.state('zoomed')
        plt.show()

    print "Done"

match_shapes.types = (str, str, int)

if __name__ == "__main__":
    run_once(match_shapes, sys.argv)
