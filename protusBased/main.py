import cv2
from operations import *
from ref import get_and_ref, get_gate_type, get_or_ref
import numpy as np

img = cv2.imread("images/test_cir2_x3.PNG")
grey_img = convert_to_grey(img)
thresh = get_thershold(grey_img)

gates = copy(thresh)
wires = copy(thresh)

fill(gates)
wires = cv2.bitwise_or(cv2.bitwise_not(gates), wires)
t = copy(wires)
wires = erode(wires, (5,5))
wires = dilate(wires, (5,5))
wires = t - wires
wires = erode(wires, (3, 3))
wires = dilate(wires, (3, 3))

borders = get_edges(gates)
img_cont = reduce_cont(get_contours(borders))
print("img", len(img_cont))

wires_cont = get_contours(wires)
print("wires", len(wires_cont))
wires_cont_filter = []
for c in wires_cont:
    if get_contour_area(c) < 50: draw_contour(wires, c, color=BLACK, fill=True)
wires = erode(wires, (3, 3))

for c in img_cont:
    gate_type = get_gate_type(c)
    if gate_type == "AND": draw_contour(img, c, color=RED)
    elif gate_type == "OR": draw_contour(img, c, color=BLUE)
    elif gate_type == "NOT": draw_contour(img, c, color=GRENN)
    elif gate_type == "XOR": draw_contour(img, c, color=MAGENTA)
    else: draw_contour(img, c, color=BLACK)

blank = np.zeros_like(wires)

num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(wires, cv2.CV_32S)
for a in range(1, num_labels):
  x = stats[a, cv2.CC_STAT_LEFT]
  y = stats[a, cv2.CC_STAT_TOP]
  w = stats[a, cv2.CC_STAT_WIDTH]
  h = stats[a, cv2.CC_STAT_HEIGHT]
  draw_rec(blank, x, y, w, h, WHITE)

blank = cv2.bitwise_and(blank, wires)

cv2.imshow("gates", gates)
cv2.imshow("thresh", thresh)
cv2.imshow("bord", borders)
cv2.imshow("img", img)
cv2.imshow("blank", blank)
cv2.imshow("wires", wires)

cv2.waitKey()