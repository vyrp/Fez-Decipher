import cv2
import os
import re
import sys

from helpers import run_once

_separator = re.compile(r"/|\\")


def moments(foldername, opname, is_bw):
    foldername = _separator.split(foldername)[0]

    print "Starting [%s]" % opname

    with open(foldername + "_" + opname + ".txt", "w") as out_file:
        for filename in os.listdir(foldername):
            img = cv2.imread(os.path.join(foldername, filename), 0)
            moment = cv2.moments(img, is_bw)

            out_file.write("=== " + filename + " ===\n\n")

            for item in ["m00", "m10", "m01", "m20", "m11", "m02", "m30", "m21", "m12", "m03"]:
                out_file.write("%s: %012.1f\n" % (item, moment[item]))
            out_file.write("\n")

            for item in ["mu20", "mu11", "mu02", "mu30", "mu21", "mu12", "mu03"]:
                out_file.write("%s: %012.1f\n" % (item, moment[item]))
            out_file.write("\n")

            for item in ["nu20", "nu11", "nu02", "nu30", "nu21", "nu12", "nu03"]:
                out_file.write("%s: %012.8f\n" % (item, moment[item]))
            out_file.write("\n")

    print "Done"

moments.types = (str, str, bool)

if __name__ == "__main__":
    run_once(moments, sys.argv)
