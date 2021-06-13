import cv2
from operations import *
from ref import get_gate_type
import numpy as np

img = cv2.imread("images/test_cir2_x3.PNG")               # load the circuit colored image 
grey_img = convert_to_grey(img)                           # convert image to grey scale
thresh = get_thershold(grey_img)                          # convert it to binary image

gates = copy(thresh)                                      # we will fill the gates in this image
wires = copy(thresh)                                      # we will operate on wires in this image

fill(gates)                                               # fill the gates to get the contours arround them

wires = cv2.bitwise_or(cv2.bitwise_not(gates), wires)     # the binary image with the gates filled
t = copy(wires)                                           # temp image of binary image with gate filled
wires = erode(wires, (5,5))
wires = dilate(wires, (5,5))
wires = t - wires                                         # get the wires only with some noise
wires = erode(wires, (3, 3))                              # remove the noise
wires = dilate(wires, (3, 3))

# remove further noise in the wires by detecting the low area contours which resembles the noise
wires_cont = get_contours(wires)
print("wires", len(wires_cont))
wires_cont_filter = []
for c in wires_cont:
    if get_contour_area(c) < 50: draw_contour(wires, c, color=BLACK, fill=True)
wires = erode(wires, (3, 3))

borders = get_edges(gates)                                # get the borders of the filled gates image
img_cont = reduce_cont(get_contours(borders))             # extract the contours to operate arround them
print("Number of contours for gates", len(img_cont))      # display number of contours (for debuging) 

# get the type of the gate based on comparing contours
for c in img_cont:
    gate_type = get_gate_type(c)
    if gate_type == "AND": draw_contour(img, c, color=RED)
    elif gate_type == "OR": draw_contour(img, c, color=BLUE)
    elif gate_type == "NOT": draw_contour(img, c, color=GRENN)
    else: draw_contour(img, c, color=BLACK)


# get the connected nodes
nodes = get_connected_nodes(wires, get_corners(wires))    # get the corners in the wires
for node in nodes:                                        # used the corner pointts to detect the connected nodes
    c = RANDOM_COLOR()
    for p in node:
        draw_cir(img, p, 10, c, True)


cv2.imshow("gates", gates)
cv2.imshow("thresh", thresh)
cv2.imshow("bord", borders)
cv2.imshow("img", img)
cv2.waitKey() 
