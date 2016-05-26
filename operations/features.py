import cv2
from helpers import run_once
from matplotlib import pyplot as plt
import numpy as np
import sys


def corners(img_gray, img_color):
    gray = np.float32(img_gray)
    corners = cv2.cornerHarris(gray, 2, 3, 0.04)

    corners = cv2.dilate(corners, None)

    result = img_color.copy()
    result[corners > 0.01 * corners.max()] = [0, 0, 255]
    return result


def sift_points(img_gray, img_color):
    sift = cv2.Feature2D_create("SIFT")
    keypoints = sift.detect(img_gray, None)
    return cv2.drawKeypoints(img_gray, keypoints, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)


def surf_points(img_gray, img_color, upright):
    surf = cv2.Feature2D_create("SURF")
    surf.setBool('upright', upright)
    keypoints = surf.detect(img_gray, None)
    return cv2.drawKeypoints(img_gray, keypoints, None, (255, 0, 0), 4)


def orb_points(img_gray, img_color):
    orb = cv2.Feature2D_create("ORB")
    orb.setInt("patchSize", 7)
    orb.setInt("edgeThreshold", 7)
    keypoints = orb.detect(img_gray, None)
    return cv2.drawKeypoints(img_gray, keypoints, None, (255, 0, 0), 4)


def features(filename, upright):
    print "Starting [features]"

    img_color = cv2.imread(filename)
    img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

    # img_result = corners(img_gray, img_color)
    # img_result = sift_points(img_gray, img_color)
    # img_result = surf_points(img_gray, img_color, eval(upright))
    img_result = orb_points(img_gray, img_color)

    plt.imshow(img_result)
    plt.show()

    print "Done"

features.types = (str, str)

if __name__ == "__main__":
    run_once(features, sys.argv)
