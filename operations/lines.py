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

    # Paint ideal division lines
    img_color = cv2.imread(filename)
    for row in range(0, h+1, cell_h):
        for col in range(0, w):
            img_color[first_row + row, first_col + col] = [255, 0, 0]

    for col in range(0, w+1, cell_w):
        for row in range(0, h):
            img_color[first_row + row, first_col + col] = [255, 0, 0]

    cv2.imwrite(filename, img_color)

to_bits.types = (str,)

if __name__ == "__main__":
    run_once(to_bits, sys.argv)
