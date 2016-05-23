import cv2
import os
import re
import sys

from helpers import run_once

_separator = re.compile(r"/|\\")


def match_shapes(foldername, opname):
    foldername = _separator.split(foldername)[0]

    print "Starting [%s]" % opname

    with open(foldername + "_" + opname + ".txt", "w") as out_file:
        filenames = os.listdir(foldername)
        imgs = [cv2.imread(os.path.join(foldername, filename), 0) for filename in filenames]

        max_len = max(map(len, filenames)) + 2
        format_str = (("%" + str(max_len) + "s") * (len(filenames) + 1)) + "\n"
        format_f = "%" + str(max_len) + "s" + (("%" + str(max_len) + ".6f") * len(filenames)) + "\n"
        for method in range(1, 4):
            matches = [0] * len(imgs)
            for idx, img1 in enumerate(imgs):
                matches[idx] = [cv2.matchShapes(img1, img2, method, 0) for img2 in imgs]

            out_file.write("=== Method %d ===\n\n" % method)
            out_file.write(format_str % tuple([""] + filenames))
            for filename, line in zip(filenames, matches):
                out_file.write(format_f % tuple([filename] + line))
            out_file.write("\n")

    print "Done"

match_shapes.types = (str, str)

if __name__ == "__main__":
    run_once(match_shapes, sys.argv)
