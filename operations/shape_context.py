import cv2
import os
import re
import sys

from helpers import run_once

_separator = re.compile(r"/|\\")


def get_contour(img_color):
    img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
    img_bw = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return cv2.findContours(img_bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]


def shape_context(foldername, opname):
    foldername = _separator.split(foldername)[0]

    print "Starting [%s]" % opname

    with open(foldername + "_" + opname + ".txt", "w") as out_file:
        filenames = os.listdir(foldername)
        imgs = [cv2.imread(os.path.join(foldername, filename)) for filename in filenames]
        contours = map(get_contour, imgs)

        dists = [0] * len(contours)
        comparer = cv2.createShapeContextDistanceExtractor()
        for idx, c1 in enumerate(contours):
            dists[idx] = [comparer.computeDistance(c1[0], c2[0]) for c2 in contours]

        max_len = max(map(len, filenames)) + 2
        format_str = (("%" + str(max_len) + "s") * (len(filenames) + 1)) + "\n"
        format_f = "%" + str(max_len) + "s" + (("%" + str(max_len) + ".6f") * len(filenames)) + "\n"

        out_file.write(format_str % tuple([""] + filenames))
        for filename, line in zip(filenames, dists):
            out_file.write(format_f % tuple([filename] + line))
        out_file.write("\n")

    print "Done"

shape_context.types = (str, str)

if __name__ == "__main__":
    run_once(shape_context, sys.argv)
