import cv2
import numpy as np

circuit_img = cv2.imread("Images\\test.jpg", 0)
and_img     = cv2.imread("Images\\and.jpg", 0)

circuit_img = cv2.resize(circuit_img, (circuit_img.shape[1]//2, circuit_img.shape[0]//2))
and_img     = cv2.resize(and_img, (and_img.shape[1]//2, and_img.shape[0]//2))

circuit_img = cv2.adaptiveThreshold(circuit_img, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,5)
and_img     = cv2.adaptiveThreshold(and_img, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,5)

cv2.medianBlur(circuit_img, 11)
cv2.medianBlur(and_img, 11)

cv2.imshow("Main Circuit", circuit_img)
cv2.imshow("And gate", and_img)

cv2.waitKey(0)
