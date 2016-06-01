import cv2
import matplotlib.pyplot as plt
import os
# import shutil
import sys

from collections import defaultdict


def get_symbol_positions(img):
    is_in_symbol = False
    start_line = None
    symbols = []
    for line_number, has_symbol in enumerate([any(line) for line in img]):
        if has_symbol and not is_in_symbol:
            is_in_symbol = True
            start_line = line_number
            continue
        if not has_symbol and is_in_symbol:
            is_in_symbol = False
            symbols.append((start_line, line_number))
    return symbols


def to_bits(img):
    """
    Gets the bitwise decimal representation of the symbol in <img>.
    <img> can have any size, but is interpreted as a matrix of 5x5 cells,
    where each cell is either black or white.
    In the binary representation, white cells are 1, and black are 0.

    Returns an integer.
    """

    # Cell sizes
    h, w = img.shape
    assert w % 5 == 0 and h % 5 == 0, "Error! Image sizes not divisible by 5."

    cell_w = w / 5
    cell_h = h / 5

    # Create bitwise representation, by taking the pixel in the middle of each cell
    bits = 0
    for row in range(cell_h / 2, h, cell_h):
        for col in range(cell_w / 2, w, cell_w):
            bits = (bits << 1) | int(img[row, col] > 0)

    return bits


def print_image_with_symbols_border(img_color_resized, symbols, filename):
    for row in symbols:
        for rectangle in row:
            cv2.rectangle(img_color_resized, rectangle[0], rectangle[1], (0, 0, 255), 2)

    cv2.imwrite(os.path.join("out", filename), img_color_resized)
    print os.path.join("out", filename)


def to_matrix(fullpath):
    img_gray = cv2.imread(fullpath, 0)
    img_bw = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    img_bw_resized = cv2.resize(img_bw, (0, 0), fx=10, fy=10, interpolation=cv2.INTER_NEAREST)

    # Making background black
    if img_bw_resized[0, 0]:
        img_bw_resized = ~img_bw_resized

    # Find symbols positions
    symbols_y = get_symbol_positions(img_bw_resized)
    symbols_x = get_symbol_positions(img_bw_resized.T)

    # Translate each symbol to its bitwise decimal representation
    symbols = [[to_bits(img_bw_resized[value_y[0]: value_y[1], value_x[0]: value_x[1]])
                for value_x in symbols_x]
               for value_y in symbols_y]

    # img_color = cv2.imread(fullpath)
    # img_color_resized = cv2.resize(img_color,(0, 0),fx=10,fy=10,interpolation=cv2.INTER_NEAREST)
    # print_image_with_symbols_border(
    #     img_color_resized,
    #     [[tuple(zip(value_x, value_y)) for value_x in symbols_x] for value_y in symbols_y],
    #     os.path.basename(fullpath)
    # )

    return symbols


def write_symbol_bits_to_file(symbols, filename):
    with open(os.path.join("out", filename + "_bits.txt"), "w") as out_file:
        text = []
        for line_of_bits in symbols:
            line = []
            for bits in line_of_bits:
                binary = bin(bits)[2:]
                line.append(("0" * (25 - len(binary))) + binary)

            text.append(" ".join(line))

        out_file.write("\n".join(text))


def decipher_symbols(foldername):
    """
    Usage:
        decipher_symbols.py <foldername:str>

    This script deciphers the symbols from the images in <folder>,
    and writes the solution in folder "symbols".
    """

    assert os.path.isdir(foldername), foldername + " doesn't exist."

    print "== Starting =="

    counts = defaultdict(int)
    for filename in os.listdir(foldername):
        print filename
        symbols = to_matrix(os.path.join(foldername, filename))
        # write_symbol_bits_to_file(symbols, filename)
        for line in symbols:
            for symbol in line:
                counts[symbol] += 1

    symbols = counts.keys()
    symbols.remove(0)
    symbols.sort(key=lambda s: counts[s], reverse=True)
    ordered_counts = [counts[s] for s in symbols]
    total = float(sum(ordered_counts))
    frequencies = [c / total for c in ordered_counts]
    xs = range(1, len(symbols) + 1)

    print "Stats:"
    print "    max: %d" % counts[symbols[0]]
    print "    min: %d" % counts[symbols[-1]]
    print "    # letters: %d" % len(symbols)
    print "    # symbols: %.0f" % total

    plt.bar(xs, frequencies, 0.5)
    plt.xlabel("Symbol decimal")
    plt.xticks(xs, [str(s) for s in symbols], rotation=70)
    plt.ylabel("Frequencies")
    plt.grid(True)
    plt.show()

    print "== Ended =="

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print decipher_symbols.__doc__
        exit(1)
    decipher_symbols(sys.argv[1])
