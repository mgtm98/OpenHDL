from operations import *
import cv2

AND_PATH = "images/and.PNG"
OR_PATH = "images/or.PNG"
NOT_PATH = "images/not.PNG"
XOR_PATH = "images/xor.PNG"


def get_ref_contour(path):
    img = cv2.imread(path)
    grey_img = convert_to_grey(img)
    thresh1 = get_thershold(grey_img)
    fill(thresh1)
    borders = get_edges(thresh1)
    and_cont = reduce_cont(get_contours(borders))
    return and_cont[0]


def get_and_ref(): return get_ref_contour(AND_PATH)
def get_or_ref(): return get_ref_contour(OR_PATH)
def get_not_ref(): return get_ref_contour(NOT_PATH)
def get_xor_ref(): return get_ref_contour(XOR_PATH)

def get_gate_type(cont):
    and_score = get_cont_similarity(cont, get_and_ref())
    or_score = get_cont_similarity(cont, get_or_ref())
    not_score = get_cont_similarity(cont, get_not_ref())
    xor_score = get_cont_similarity(cont, get_xor_ref())
    print(and_score, or_score, not_score, xor_score)
    min_score = min(and_score, or_score, not_score, xor_score)
    if min_score > 0.1: return "NONE"
    if min_score == and_score: return "AND"
    elif min_score == or_score: return "OR"
    elif min_score == xor_score: return "XOR"
    elif min_score == not_score: return "NOT"