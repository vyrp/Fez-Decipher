from helpers import run
import sys


def invert():
    return lambda img: 255 - img

invert.types = ()

if __name__ == "__main__":
    run(invert, sys.argv)
