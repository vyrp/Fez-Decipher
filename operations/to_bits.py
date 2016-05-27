import cv2
from helpers import run_once
import sys


def to_bits(filename):
    img = cv2.imread(filename, 0)

    # Find first and last lines of the symbol
    rows = [any(img[idx, :]) for idx in range(img.shape[0])]
    first_row = rows.index(True)
    last_row = rows.index(False, first_row)
    h = last_row - first_row

    # Find first and last columns of the symbol
    cols = [any(img[:, idx]) for idx in range(img.shape[1])]
    first_col = cols.index(True)
    last_col = cols.index(False, first_col)
    w = last_col - first_col

    # Cell sizes
    assert w % 5 == 0 and h % 5 == 0, "Error! Image sizes not divisible by 5."

    cell_w = w / 5
    cell_h = h / 5

    # Create matrix of ASCII and bitwise representation, by taking the middle of each cell
    bits = []
    number = 0
    for row in range(cell_h / 2, h, cell_h):
        for col in range(cell_w / 2, w, cell_w):
            bit = img[first_row + row, first_col + col] > 0
            bits.append("#" if bit else ".")
            number <<= 1
            number |= int(bit)

    print "\n" + filename + ":\n"
    print "\n".join(["".join(bits[idx: idx + 5]) for idx in range(0, 25, 5)]) + "\n"
    print "decimal: " + str(number)
    print "binary: " + bin(number)[2:]

to_bits.types = (str,)

if __name__ == "__main__":
    run_once(to_bits, sys.argv)
