import cv2
from helpers import run
import sys


def edges(low, high):
    return lambda img: cv2.Canny(img, low, high)

edges.types = (int, int)

if __name__ == "__main__":
    run(edges, sys.argv)
