import cv2
from helpers import run
import sys


def contours():
    def contours_fn(img_color):
        result = img_color.copy()

        # Find contours
        img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
        img_bw = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        contours = cv2.findContours(img_bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]

        # Draw contours
        colors = [255, 0, 0]
        for c in contours:
            cv2.drawContours(result, [c], 0, tuple(colors), 1)
            colors.append(colors.pop(0))

        return result
    return contours_fn

contours.types = ()

if __name__ == "__main__":
    run(contours, sys.argv)
