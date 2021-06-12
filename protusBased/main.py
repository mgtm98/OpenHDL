import cv2
from operations import *
from ref import get_and_ref, get_gate_type, get_or_ref
import numpy as np

img = cv2.imread("images/test_cir1.PNG")
grey_img = convert_to_grey(img)
thresh1 = get_thershold(grey_img)
fill(thresh1)

borders = get_edges(thresh1)
img_cont = reduce_cont(get_contours(borders))
print(len(img_cont))

for c in img_cont:
    gate_type = get_gate_type(c)
    if gate_type == "AND": draw_contour(img, c, color=RED)
    elif gate_type == "OR": draw_contour(img, c, color=BLUE)
    elif gate_type == "NOT": draw_contour(img, c, color=GRENN)
    elif gate_type == "XOR": draw_contour(img, c, color=MAGENTA)


cv2.imshow("orig", thresh1)
cv2.imshow("bord", borders)
cv2.imshow("img", img)

cv2.waitKey()