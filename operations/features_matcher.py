import cv2
from draw_matches import draw_matches
from helpers import run_once
import sys


def match(filename1, filename2):
    print "Starting [match]"

    # Compute descriptors
    img1 = cv2.imread(filename1, 0)  # queryImage
    img2 = cv2.imread(filename2, 0)  # trainImage
    img1_color = cv2.imread(filename1)
    img2_color = cv2.imread(filename2)

    surf = cv2.Feature2D_create("SURF")
    surf.setBool('upright', True)
    kp1, des1 = surf.detectAndCompute(img1, None)
    kp2, des2 = surf.detectAndCompute(img2, None)

    # Match
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda m: m.distance)

    # Draw
    draw_matches(img1_color, kp1, img2_color, kp2, matches[:10])

    print "Done"

match.types = (str, str)

if __name__ == "__main__":
    run_once(match, sys.argv)
