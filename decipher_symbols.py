import cv2
import os
import shutil
import sys


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


def print_image_with_symbols_border(img_color_resized, symbols, filename):
    for row in symbols:
        for rectangle in row:
            cv2.rectangle(img_color_resized, rectangle[0], rectangle[1], (0, 0, 255), 1)

    cv2.imwrite(os.path.join("out", filename), img_color_resized)
    print os.path.join("out", filename)


def to_bits(symbol, img):
    """
    Gets the bitwise decimal representation of <symbol>,
    passed as a rectangle in ((xstart, ystart), (xend, yend)) form.

    Returns an integer.
    """

    # Find first and last lines of the symbol
    first_row = symbol[0][1]
    last_row = symbol[1][1]
    h = last_row - first_row

    # Find first and last columns of the symbol
    first_col = symbol[0][0]
    last_col = symbol[1][0]
    w = last_col - first_col

    # Cell sizes
    assert w % 5 == 0 and h % 5 == 0, "Error! Image sizes not divisible by 5."

    cell_w = w / 5
    cell_h = h / 5

    # Create bitwise representation, by taking the pixel in the middle of each cell
    bits = 0
    for row in range(cell_h / 2, h, cell_h):
        for col in range(cell_w / 2, w, cell_w):
            bit = img[first_row + row, first_col + col] > 0
            bits = (bits << 1) | int(bit)

    return bits


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

    if not os.path.isdir(foldername):
        print foldername + " doesn't exist."
        exit(1)

    if os.path.isdir("out"):
        shutil.rmtree("out")
    os.mkdir("out")

    print "== Starting ==", os.getcwd()
    for filename in os.listdir(foldername):
        img_color = cv2.imread(os.path.join(foldername, filename))
        img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
        img_bw = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        img_bw_resized = cv2.resize(img_bw, (0, 0), fx=10, fy=10, interpolation=cv2.INTER_NEAREST)
        # img_color_resized=cv2.resize(img_color,(0,0),fx=10,fy=10,interpolation=cv2.INTER_NEAREST)

        # Making background black
        if img_bw_resized[0, 0]:
            img_bw_resized = ~img_bw_resized

        # Find symbols positions
        symbols_y = get_symbol_positions(img_bw_resized)
        symbols_x = get_symbol_positions(img_bw_resized.T)

        symbol_positions = [None] * len(symbols_y)
        for idx_y, value_y in enumerate(symbols_y):
            symbol_positions[idx_y] = [None] * len(symbols_x)
            for idx_x, value_x in enumerate(symbols_x):
                # ((xstart, ystart), (xend, yend))
                symbol_positions[idx_y][idx_x] = tuple(zip(value_x, value_y))

        # Translate each symbol to its bitwise decimal representation
        symbols = [[to_bits(symbol, img_bw_resized) for symbol in line]
                   for line in symbol_positions]

        write_symbol_bits_to_file(symbols, filename)

        # Write a txt

    print "== Ended ==\n"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print decipher_symbols.__doc__
        exit(1)
    decipher_symbols(sys.argv[1])
