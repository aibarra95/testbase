# python test_grader.py --image images/test_01.png

from imutils.perspective import four_point_transform
from imutils import contours
import sys
import numpy as np
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
args = vars(ap.parse_args())

ANSWER_KEY = {0: 1, 1: 4, 2: 0, 3: 3, 4: 1}
correct1 = 0;
correct2 = 0;
correct3 = 0;
correct4 = 0;
correct5 = 0;
CORRECT_STATS = {0: correct1, 1: correct2, 2: correct3, 3:correct4, 4:correct5 }

# finding edges of exam
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(blurred, 75, 200)
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
docCnt = None

# making sure the exam is found
if len(cnts) > 0:
	cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

	for c in cnts:
		# approximate the contour
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)

		# four contours = found exam
		if len(approx) == 4:
			docCnt = approx
			break

# finding top-down view of scantron 
paper = four_point_transform(image, docCnt.reshape(4, 2))
warped = four_point_transform(gray, docCnt.reshape(4, 2))
thresh = cv2.threshold(warped, 0, 255,
	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

# assinging questions to contours(bubbles)
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
questionCnts = []

for c in cnts:
	(x, y, w, h) = cv2.boundingRect(c)
	ar = w / float(h)

	if w >= 20 and h >= 20 and ar >= 0.9 and ar <= 1.1:
		questionCnts.append(c)

questionCnts = contours.sort_contours(questionCnts,
	method="top-to-bottom")[0]
correct = 0

for (q, i) in enumerate(np.arange(0, len(questionCnts), 5)):
	cnts = contours.sort_contours(questionCnts[i:i + 5])[0]
	bubbled = None

	for (j, c) in enumerate(cnts):
		mask = np.zeros(thresh.shape, dtype="uint8")
		cv2.drawContours(mask, [c], -1, 255, -1)

		mask = cv2.bitwise_and(thresh, thresh, mask=mask)
		total = cv2.countNonZero(mask)

		if bubbled is None or total > bubbled[0]:
			bubbled = (total, j)
	
	#color right answer
	color = (0, 255, 0)
	k = ANSWER_KEY[q]

	# check to see if the bubbled answer is correct
	if k == bubbled[1]:
		color = (0, 255, 0)
		correct += 1

	# draw the outline of the correct answer on the test
	cv2.drawContours(paper, [cnts[k]], -1, color, 3)

score = (correct / 5.0) * 100
print("[INFO] score: {:.2f}%".format(score))
cv2.putText(paper, "{:.2f}%".format(score), (10, 30),
	cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
cv2.imshow("Original", image)
cv2.imshow("Exam", paper)
c = cv2.waitKey(0)
if 'q' == chr(c&255):
	sys.exit(0)
