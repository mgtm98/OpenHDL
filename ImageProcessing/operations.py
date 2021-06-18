import cv2
import numpy as np
from itertools import product
from random import randint
import math

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

def get_adaptive_threshold(img):
    return cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,7,2)


def fill(img):
    cv2.floodFill(img, None, seedPoint=(0, 0), newVal=(255, 255, 255))


def get_edges(img, lower_limit=125, upper_limit=175):
    return cv2.Canny(img, lower_limit, upper_limit)


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
        x, y, w, h = cv2.boundingRect(c)
        if x in x_list and y in y_list and w in w_list and h in h_list:
            continue
        else:
            out.append(c)
            x_list.append(x)
            y_list.append(y)
            w_list.append(w)
            h_list.append(h)
    return out


def draw_contour(img, c, color=WHITE, pen=2, fill=False):
    x, y, w, h = cv2.boundingRect(c)
    if fill: pen = -1
    cv2.rectangle(img, (x, y), (x + w, y + h), color, pen)


def get_bounding_box(c):
    return cv2.boundingRect(c)


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
    cv2.rectangle(img, (x, y), (x + w, y + h), color, pen)


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


def get_lines(img, rho=1, theta=np.pi / 180, threshold=100):
    return cv2.HoughLinesP(img, rho, theta, threshold, 1, 10)


def __search(img, test, point, dx, dy):
    x = [point[0] + dx, point[0], point[0] - dx]
    y = [point[1] + dy, point[1], point[1] - dy]
    points = list(product(x, y))
    points.remove((point[0], point[1]))
    out = []
    for p in points:
        if img[p[1], p[0]]:
            out.append(p)
            draw_cir(test, p, 3, color=WHITE, fill=True)
            draw_cir(img, p, 3, color=BLACK, fill=True)
            # cv2.imshow("test", test)
            # cv2.imshow("img", img)
            # cv2.waitKey()
    return out


def get_connected_nodes(img, corners):
    test = np.zeros_like(img)
    f_out = {}
    for i in range(len(corners)):
        corner = corners[i]
        draw_cir(test, corner, 3, color=WHITE, fill=True)
        # cv2.imshow("test", test)
        # cv2.waitKey()
        stack = [corner]
        terminals = []
        while True:
            # print("stack", stack)
            p = stack.pop()
            out = __search(img, test, p, 4, 4)
            stack += out
            if len(out) == 0: terminals.append(p)
            if len(stack) == 0: break
        # print("line finished", terminals)
        if len(terminals) > 1: f_out["N" + str(i)] = {"terminals": terminals}
    return f_out


def get_distance_between_points(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def reduce_nodes(nodes):
    points = []
    for n in nodes:
        for t in nodes[n]["terminals"]:
            points.append([t, n])
    for p1 in points:
        for p2 in points:
            if p1 == p2:
                continue
            else:
                distance = get_distance_between_points(p1[0], p2[0])
                # print(distance)
                if distance < 20:
                    # print("added")
                    p1.append(p2[1])
    i = 0
    node_map = {}
    for p in points:
        if len(p) > 2:
            for j in range(1, len(p)):
                if p[j] not in node_map:
                    node_map[p[j]] = "J" + str(i)
            i += 1
    out = {}
    for p in points:
        if p[1] in node_map:
            if node_map[p[1]] not in out: out[node_map[p[1]]] = {"terminals": []}
            out[node_map[p[1]]]["terminals"].append(p[0])
        else:
            if p[1] not in out: out[p[1]] = {"terminals": []}
            out[p[1]]["terminals"].append(p[0])
    return out


def blur(img, size):
    return cv2.GaussianBlur(img, (size, size), cv2.BORDER_DEFAULT)


def check_point_in_rec(p, search_box):
    return search_box[0] <= p[0] <= search_box[0] + search_box[2] and search_box[1] <= p[1] <= search_box[1] + \
           search_box[3]


def add_text(img, text, point, color=RANDOM_COLOR(), pen=2):
    return cv2.putText(img, text, point, cv2.FONT_HERSHEY_SIMPLEX, 1, color, pen, cv2.LINE_AA)


get_contour_area = cv2.contourArea
show = cv2.imshow
wait = cv2.waitKey