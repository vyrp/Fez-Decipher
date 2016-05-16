import cv2
import os
import shutil
import sys

def main(foldername):
    newfolder = foldername + "_bw"
    if os.path.isdir(newfolder):
        shutil.rmtree(newfolder)
    os.mkdir(newfolder)

    print "Starting"

    for filename in os.listdir(foldername):
        img = cv2.imread(os.path.join(foldername, filename))
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, bw_img = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        cv2.imwrite(os.path.join(newfolder, filename), bw_img)

    print "Done"

if __name__ == "__main__":
    main(sys.argv[1])
