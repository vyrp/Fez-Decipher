import cv2

name = "Screenshot (X).png"

print "Starting"
for i in range(33, 41):
	img = cv2.imread(name.replace("X", str(i)))
	crop_img = img[425:425+245, 875:875+225]
	gray_image = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
	thresh, bw_img = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
	print thresh
	cv2.imwrite("BlackWhite %d.png" % i, bw_img)
print "Done"
