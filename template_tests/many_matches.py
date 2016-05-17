import cv2
import numpy as np
from matplotlib import pyplot as plt
import sys

a = np.array
t = tuple

threshold = float(sys.argv[1])
template_name = sys.argv[2]

methods = ["cv2.TM_CCOEFF_NORMED", "cv2.TM_CCORR_NORMED", "cv2.TM_SQDIFF_NORMED"]

for meth in methods:
    img_rgb = cv2.imread("Cropped 33.png")
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(template_name, cv2.IMREAD_GRAYSCALE)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, eval(meth))

    if meth == "cv2.TM_SQDIFF_NORMED":
        res = 1 - res

    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, t(a(pt) - a([1, 1])), t(a(pt) + a([w, h])), (0, 0, 255), 2)

    plt.subplot(121), plt.imshow(template, cmap="gray")
    plt.title("Symbol"), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(img_rgb)
    plt.title("Matches"), plt.xticks([]), plt.yticks([])
    plt.suptitle(meth)

    plt.show()
