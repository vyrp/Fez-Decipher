from helpers import run
import sys


def crop(x, w, y, h):
    return lambda img: img[y:y+h, x:x+w]

crop.types = (int, int, int, int)

if __name__ == "__main__":
    run(crop, sys.argv)
