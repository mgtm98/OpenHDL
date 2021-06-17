import cv2
from .operations import *
from .ref import get_gate_type
import numpy as np
import pprint

import os

pp = pprint.PrettyPrinter(indent=4)
show = cv2.imshow
wait = cv2.waitKey


def extract_circuit(path):
    img = cv2.imread(path)  # load the circuit colored image
    show("original image", img)
    wait()

    grey_img = convert_to_grey(img)  # convert image to grey scale
    show("grey image", grey_img)
    wait()

    thresh = get_thershold(grey_img)  # convert it to binary image
    show("binary image", thresh)
    wait()

    gates = copy(thresh)  # we will fill the gates in this image
    wires = copy(thresh)  # we will operate on wires in this image

    fill(gates)  # fill the gates to get the contours arround them
    show("gates_filled", gates)
    wait()

    wires = cv2.bitwise_or(cv2.bitwise_not(gates), wires)  # the binary image with the gates filled()
    t = copy(wires)  # temp image of binary image with gate filled
    wires = erode(wires, (5, 5))
    wires = dilate(wires, (5, 5))
    wires = t - wires  # get the wires only with some noise
    wires = erode(wires, (3, 3))  # remove the noise
    wires = dilate(wires, (3, 3))
    show("wires", wires)
    wait()

    # remove further noise in the wires by detecting the low area contours which resembles the noise
    wires_cont = get_contours(wires)
    print("wires", len(wires_cont))

    # for c in wires_cont:
    #     if get_contour_area(c) < 50: draw_contour(wires, c, color=BLACK, fill=True)
    wires = erode(wires, (3, 3))

    borders = get_edges(gates)  # get the borders of the filled gates image
    img_cont = reduce_cont(get_contours(borders))  # extract the contours to operate arround them
    print("Number of contours for gates", len(img_cont))  # display number of contours (for debuging)

    gates_meta_data = {}

    # get the type of the gate based on comparing contours
    for i in range(len(img_cont)):
        c = img_cont[i]
        gate_type = get_gate_type(c)
        gate_name = gate_type + str(i)
        gates_meta_data[gate_name] = {
            "box": get_bounding_box(c)
        }
        p = (gates_meta_data[gate_name]["box"][0], gates_meta_data[gate_name]["box"][1])
        img = add_text(img, gate_name, p, BLACK)
        if gate_type == "AND":
            draw_contour(img, c, color=RED)
        elif gate_type == "OR":
            draw_contour(img, c, color=BLUE)
        elif gate_type == "NOT":
            draw_contour(img, c, color=GRENN)
        else:
            draw_contour(img, c, color=BLACK)

    # print("gates_meta_data", gates_meta_data)
    # print("print", p)
    # get the connected nodes
    nodes = get_connected_nodes(wires, get_corners(wires))  # get the corners in the wires
    nodes = reduce_nodes(nodes)

    for node_name in nodes:
        terminals = nodes[node_name]["terminals"]  # used the corner pointts to detect the connected nodes
        c = RANDOM_COLOR()
        for p in terminals:
            draw_cir(img, p, 10, c, True)
        img = add_text(img, node_name, terminals[0], c)

    for gate in gates_meta_data:
        box = gates_meta_data[gate]["box"]
        search_box = (box[0] - 10, box[1] - 10, box[2] + 20, box[3] + 20)
        for node_name in nodes:
            terminals = nodes[node_name]["terminals"]
            if "gate_connected" not in nodes[node_name]:
                nodes[node_name]["gate_connected"] = []
            for p in terminals:
                if check_point_in_rec(p, search_box): nodes[node_name]["gate_connected"].append(gate)

    # pp.pprint(nodes)

    gates_names = list(gates_meta_data.keys())
    gates_to_node = {i: [] for i in gates_names}
    for gate in gates_names:  # ['AND0', 'AND1', 'OR1', 'NOT2']
        for wire in nodes.keys():
            if gate in nodes[wire]['gate_connected']:
                gates_to_node[gate].append(wire)
    # pp.pprint(gates_to_node)

    for gate in gates_to_node:
        box = gates_meta_data[gate]["box"]
        search_box = (box[0] - 10, box[1] - 10, box[2] + 20, box[3] + 20)
        for i in range(len(gates_to_node[gate])):
            node = gates_to_node[gate][i]
            for t in nodes[node]["terminals"]:
                if check_point_in_rec(t, search_box):
                    gates_to_node[gate][i] = (node, t)
                    break

    # pp.pprint(gates_to_node)

    objects_in_criecuit = {}

    for gate in gates_to_node:
        if "NOT" in gate: continue
        gate_object = {}
        points = {}
        gate_to_node = gates_to_node[gate]
        for i in range(len(gate_to_node)): points[i] = gate_to_node[i][1]
        dist = []
        for i in range(1, len(gate_to_node)): dist.append(get_distance_between_points(points[0], points[i]))
        if abs(dist[0] - dist[1]) < 10:
            gate_object["inputs"] = [gate_to_node[1][0], gate_to_node[2][0]]
            gate_object["output"] = gate_to_node[0][0]
        elif dist[0] > dist[1]:
            gate_object["inputs"] = [gate_to_node[0][0], gate_to_node[2][0]]
            gate_object["output"] = gate_to_node[1][0]
        else:
            gate_object["inputs"] = [gate_to_node[0][0], gate_to_node[1][0]]
            gate_object["output"] = gate_to_node[2][0]
        objects_in_criecuit[gate] = gate_object

    for gate in gates_to_node:
        if "NOT" in gate:
            box = gates_meta_data[gate]["box"]
            x1 = box[0] - 5
            x2 = box[0] + box[2] + 5
            y1 = box[1] - 5
            y2 = box[1] + box[3] + 5
            not_img = blur(gates[y1:y2, x1:x2], 5)
            corners = get_corners(not_img)
            output_point = None
            dist = []
            for i in range(1, len(corners)): dist.append(get_distance_between_points(corners[0], corners[i]))
            if abs(dist[0] - dist[1]) < 5:
                output_point = corners[0]
            elif dist[0] > dist[1]:
                output_point = corners[2]
            else:
                output_point = corners[1]
            # draw_cir(not_img, output_point, 5)
            # cv2.imshow("not", not_img)
            output_point = (output_point[0] + x1 + 5, output_point[1] + y1 + 5)
            # draw_cir(img, output_point, 5)
            # cv2.imshow("not", img)
            points = {}
            gate_to_node = gates_to_node[gate]
            for i in range(len(gate_to_node)): points[i] = gate_to_node[i][1]
            if get_distance_between_points(points[0], output_point) < 10:
                objects_in_criecuit[gate] = {
                    "inputs": [gate_to_node[1][0]],
                    "output": gate_to_node[0][0],
                }
            else:
                objects_in_criecuit[gate] = {
                    "inputs": [gate_to_node[0][0]],
                    "output": gate_to_node[1][0],
                }
    # pp.pprint(objects_in_criecuit)
    cv2.imwrite("out.png", img)
    return objects_in_criecuit

# for gate in gates_to_wires.keys():
#     x1, y1, w, h = gates_meta_data[gate]['box']
#     x2, y2 = x1+w, y1+h
#     points = []
#     for wire in gates_to_wires[gate]:
#         for point in nodes[wire]['terminals']:
#             if abs(x1 - point[0])<=3:
#                 points.append((wire, x1))
#             elif abs(x2 - point[0]):                         # let it be "if", if we support loops
#                 points.append((wire, x2))

# cv2.imshow("gates", gates)
# cv2.imshow("thresh", thresh)
# cv2.imshow("bord", borders)
# cv2.imshow("img", img)
# cv2.waitKey()
