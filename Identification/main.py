import cv2
import numpy as np

cv = cv2

# Reading images
circuit_img = cv2.imread('./Images/test4.jpg', 0)
circuit_original_img = cv2.imread('./Images/test4.jpg')


# resize image to quarter of it's size
circuit_img = cv2.resize(
  circuit_img, (circuit_img.shape[1]//2, circuit_img.shape[0]//2))
circuit_original_img = cv2.resize(
  circuit_original_img, (circuit_original_img.shape[1]//2, circuit_original_img.shape[0]//2 ))

circuit_img =cv.Canny(circuit_img, 125,175)

# cv.imshow("after canny", circuit_img)
# cv.waitKey()

custom_kernel1 = np.array([[0,0,0,0,0],
                           [0,0,0,0,0],
                           [1,1,1,0,0],
                           [1,1,1,1,0],
                           [1,1,1,1,0]] ,np.uint8 )

#circuit_img = cv.dilate(circuit_img, cv.getStructuringElement(
 #   cv.MORPH_RECT, (5, 1)), iterations=4)

circuit_img = cv.dilate(circuit_img,custom_kernel1, iterations=3)
# cv.imshow("after dilation", circuit_img)
# cv.waitKey()

paintBucket= circuit_img.copy()

cv.floodFill(paintBucket, None, seedPoint=(0,0), newVal=(255,255,255))
# cv.imshow("after flood fill", paintBucket)
# cv.waitKey()

gates = 255-paintBucket
# cv.imshow("after flood fill", gates)
# cv.waitKey()

and_img = cv2.imread('./Images/and.jpg', 0)
and_img = cv2.resize(and_img, (and_img.shape[1]//2, and_img.shape[0]//2))
and_img = cv2.adaptiveThreshold(and_img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
and_img = cv2.medianBlur(and_img, 5)
cv2.floodFill(and_img, None, seedPoint=(0,0), newVal=(255,255,255))
and_img = 255 - and_img
# cv.imshow("and image", and_img)
# cv.waitKey()

or_img = cv2.imread('./Images/or2.jpg', 0)
or_img = cv2.resize(or_img, (or_img.shape[1]//2, or_img.shape[0]//2))
# cv.imshow("or image1", or_img)
# cv.waitKey()
or_img = cv2.adaptiveThreshold(or_img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 5)
or_img = cv2.medianBlur(or_img, 5)
# cv.imshow("or image", or_img)
# cv.waitKey()
cv2.floodFill(or_img, None, seedPoint=(0,0), newVal=(255,255,255))
or_img = 255 - or_img
# cv.imshow("or image", or_img)
# cv.waitKey()


and_cont, _ = cv2.findContours(and_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
or_cont, _ = cv2.findContours(or_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
gates_cont, _ = cv2.findContours(gates, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

print("and gates")
for c in gates_cont:
  print(cv2.matchShapes(c,and_cont[0],1,0.0))
  if cv2.matchShapes(c,and_cont[0],1,0.0) < 0.2:
    rect = cv2.boundingRect(c)
    x,y,w,h = rect
    cv2.rectangle(circuit_original_img,(x,y),(x+w,y+h),(255,0,0),2)

print("or gates")
for c in gates_cont:
  print(cv2.matchShapes(c,or_cont[0],1,0.0))
  if cv2.matchShapes(c,or_cont[0],1,0.0) < 0.1:
    rect = cv2.boundingRect(c)
    x,y,w,h = rect
    cv2.rectangle(circuit_original_img,(x,y),(x+w,y+h),(0,255,0),2)

cv.imshow("Identified", circuit_original_img)
cv.waitKey()

# circuit_img = paintBucket + circuit_img
# cv.imshow("after flood fill", circuit_img)
# cv.waitKey()


# #detect connected components from paintbucket and draw big rectangles over them in circuit image
# # to be acurate rectangle dim = detected dimension + 2* edge -rect thickness (~ 30/2 pixel)  


# num_labels, labels, stats, centroids = cv.connectedComponentsWithStats(paintBucket)

# for i in range (1, num_labels) : 

#     x = stats[i, cv2.CC_STAT_LEFT] - 15
#     y = stats[i, cv2.CC_STAT_TOP] - 15
#     w = stats[i, cv2.CC_STAT_WIDTH] + 30
#     h = stats[i, cv2.CC_STAT_HEIGHT] + 30

#   # drawing rectangles over gates 
#     cv.rectangle (circuit_original_img , (x,y) , (x+w,y+h)
#                                           ,  (125,0,255) , thickness =2) 

# cv.imshow("after drawing gates", circuit_original_img)
# cv.waitKey()


# # dilate paint bucket and subtract from original image 

# custom_kernel2 = np.array([[1,1,1,0,0],
#                            [1,1,1,1,0],
#                            [1,1,1,1,1],
#                            [1,1,1,1,0],
#                            [1,1,1,0,0]] ,np.uint8 )



# #wires should ve the wires only

# #wires = total binary image && ~( dilated paintbucket)
# wires= circuit_img.copy()
# wires = cv.bitwise_and(cv.bitwise_not(
#                             cv.dilate(paintBucket.copy(),custom_kernel2, iterations=10) ), 
#                             wires )

# # some dots appear from previous op - > errosion

# wires = cv2.erode(wires, (5, 5) , iterations=7)

# # detecting wires



# num_labels, labels, stats, centroids = cv.connectedComponentsWithStats(wires)

# print(num_labels)
# for i in range (1, num_labels) : 

#     x = stats[i, cv2.CC_STAT_LEFT] - 15
#     y = stats[i, cv2.CC_STAT_TOP] - 15
#     w = stats[i, cv2.CC_STAT_WIDTH] + 30
#     h = stats[i, cv2.CC_STAT_HEIGHT] + 30

#   # drawing rectangles over gates 
#   #should add condition to reject wires beneath certain area (noise)
#     cv.rectangle (circuit_original_img , (x,y) , (x+w,y+h)
#                                           ,  (25,250,125) , thickness =2) 
  

# #cv2.imshow("Count", and_img)
# cv.imshow("Circuit", circuit_img)
# cv.imshow("wires", wires)
# cv.imshow("filling", paintBucket)
# cv.imshow("gatesdetection", circuit_original_img)
# cv.waitKey(0)
cv.destroyAllWindows()
