import cv2
import numpy as np
from itertools import product
from random import randint

BLUE = (255, 0, 0)
GRENN = (0, 255, 0)
RED = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
MAGENTA = (255, 0, 255)
RANDOM_COLOR = lambda: (int(randint(0, 255)), int(randint(0, 255)), int(randint(0, 255)))

def get_thershold(img, upper_limit=255, lower_limit=127, type=cv2.THRESH_BINARY_INV):
    _, t = cv2.threshold(img, lower_limit, upper_limit, type)
    return t

def fill(img):
    cv2.floodFill(img, None, seedPoint=(0,0), newVal=(255,255,255))

def get_edges(img, lower_limit=125, upper_limit=175):
    return  cv2.Canny(img, lower_limit, upper_limit)

def get_contours(img):
    cont, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    return cont

def reduce_cont(contours):
    x_list = []
    y_list = []
    w_list = []
    h_list = []
    out = []
    for c in contours:
        x,y,w,h = cv2.boundingRect(c)
        if x in x_list and y in y_list and w in w_list and h in h_list: continue
        else:
            out.append(c)
            x_list.append(x)
            y_list.append(y)
            w_list.append(w)
            h_list.append(h)
    return out
    
def draw_contour(img, c, color=WHITE, pen=2, fill=False):
    x,y,w,h = cv2.boundingRect(c)
    if fill: pen = -1
    cv2.rectangle(img, (x, y), (x + w, y + h), color, pen)

def convert_to_grey(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def get_cont_similarity(cont, ref_cont):
    return cv2.matchShapes(cont, ref_cont, 1, 0.0)

def copy(img):
    return img.copy()

def dilate(img, kernel):
    kernel = np.ones(kernel)
    return cv2.dilate(img, kernel)

def erode(img, kernel):
    kernel = np.ones(kernel)
    return cv2.erode(img, kernel)

def draw_rec(img, x, y, w, h, color=BLACK, fill=False, pen=2):
    pen = pen if not fill else -1
    cv2.rectangle(img, (x, y), (x+w, y+h), color, pen)

def draw_cir(img, center, r, color=BLACK, fill=False, pen=2):
    pen = pen if not fill else -1
    cv2.circle(img, center, r, color, pen)

def get_corners(img):
    corners = cv2.goodFeaturesToTrack(img, 100, 0.01, 10)
    corners = np.int0(corners)
    corners = corners.squeeze().tolist()
    out = []
    for c in corners:
      out.append((c[0], c[1]))
    return out

def get_lines(img, rho=1, theta = np.pi/180, threshold=100):
    return cv2.HoughLinesP(img, rho, theta, threshold, 1, 10)

def __search(img, test, point, dx, dy):
    x = [point[0]+dx, point[0], point[0]-dx]
    y = [point[1]+dy, point[1], point[1]-dy]
    points = list(product(x, y))
    points.remove((point[0], point[1]))
    out = []
    for p in points:
       if img[p[1], p[0]]:
          out.append(p)
          draw_cir(test, p, 3, color=WHITE, fill=True)
          draw_cir(img, p, 3, color=BLACK, fill=True)    
          # cv2.imshow("test", test)
          # cv2.waitKey()
    return out

def get_connected_nodes(img, corners):
    test = np.zeros_like(img)
    f_out = []
    for corner in corners:
        draw_cir(test, corner, 3, color=WHITE, fill=True)
        # cv2.imshow("test", test)
        # cv2.waitKey()
        stack = [corner]
        terminals = []
        while True:
            p = stack.pop()
            out = __search(img, test, p, 4, 4)
            stack += out
            if len(out) == 0: terminals.append(p)
            if len(stack) == 0: break
        # print("line finished", terminals)
        if len(terminals) > 1: f_out.append(terminals)
    return f_out

get_contour_area = cv2.contourArea

