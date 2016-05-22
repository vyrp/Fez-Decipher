import cv2
from helpers import run
import sys


def bw():
    def bw_fn(img):
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return bw_fn

bw.types = ()

if __name__ == "__main__":
    run(bw, sys.argv)
