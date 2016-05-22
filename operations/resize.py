import cv2
from helpers import run
import sys


def resize(scale):
    return lambda img: cv2.resize(img, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST)

resize.types = (float,)

if __name__ == "__main__":
    run(resize, sys.argv)
