import cv2

def main(filenames, x, w, y, h):
    print "Starting"
    for filename in filenames:
        img = cv2.imread(filename)
        crop_img = img[y:y+h, x:x+w]
        cv2.imwrite("Cropped_" + filename, crop_img)
    print "Done"

if __name__ == "__main__":
    main(["Screenshot (%d).png" % i for i in range(33, 42)], 530, 605, 365, 370)
