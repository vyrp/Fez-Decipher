import cv2
import re
import sys

from helpers import run_once

_separator = re.compile(r"/|\\")


def get_contour(img_color):
    img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
    img_bw = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return cv2.findContours(img_bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]


def compare(file1, file2):
    print "Starting [compare]"

    c1 = get_contour(cv2.imread(file1))
    c2 = get_contour(cv2.imread(file2))

    # Warning: bug in OpenCV 3.1.0. Always return 0.
    print cv2.createShapeContextDistanceExtractor().computeDistance(c1[0], c2[0])

    print "Done"

compare.types = (str, str)

if __name__ == "__main__":
    run_once(compare, sys.argv)
