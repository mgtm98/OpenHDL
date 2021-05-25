import cv2
import numpy as np

cv = cv2

circuit_img = cv2.imread('./Images/test.jpg', 0)
circuit_original_img = cv2.imread('./Images/test.jpg')

and_img = cv2.imread('./Images/and.jpg', 0)

circuit_img = cv2.resize(
    circuit_img, (circuit_img.shape[1]//2, circuit_img.shape[0]//2))

circuit_original_img = cv2.resize(
    circuit_original_img, (circuit_original_img.shape[1]//2, circuit_original_img.shape[0]//2 ))
print(circuit_original_img.shape)
and_img = cv2.resize(and_img, (and_img.shape[1]//2, and_img.shape[0]//2))
'''
circuit_img = cv2.adaptiveThreshold(
    circuit_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 5)
and_img = cv2.adaptiveThreshold(
    and_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 5)

circuit_img = cv2.medianBlur(circuit_img, 5)
and_img = cv2.medianBlur(and_img, 3)
'''

#_,circuit_img = cv.threshold(circuit_img,120,175,cv.THRESH_BINARY_INV)
circuit_img =cv.Canny(circuit_img, 125,175)


print(circuit_img.shape)




#circuit_img = cv2.erode(circuit_img, (9, 9))
#and_img     = cv2.erode(and_img, (9, 9))

# circuit_img = cv2.Canny(circuit_img, 120, 170)
# and_img     = cv2.Canny(and_img, 120, 170)

#contours_and, hir = cv2.findContours(and_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#contours_cir, hir = cv2.findContours(circuit_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
'''
print(len(contours_and))

matched = {}
for c in contours_cir:
  ret = cv2.matchShapes(c, contours_and[0], 1, 0.0)
  matched[ret] = c

for ret in matched:
  c = matched[ret]
  i = np.copy(circuit_img)
  x,y,w,h = cv2.boundingRect(c)
  cv2.rectangle(i,(x,y),(x+w,y+h),(255,255,255),2)
  cv2.imshow(str(ret), i)
'''
# # img = np.zeros_like(and_img)
# # cv2.drawContours(img, contours[1], -1, (255,255,255), -1)



###############################################################

custom_kernel1 = np.array([[0,0,0,0,0],
                           [0,0,0,0,0],
                           [1,1,1,0,0],
                           [1,1,1,1,0],
                           [1,1,1,1,0]] ,np.uint8 )

#circuit_img = cv.dilate(circuit_img, cv.getStructuringElement(
 #   cv.MORPH_RECT, (5, 1)), iterations=4)

circuit_img = cv.dilate(circuit_img,custom_kernel1, iterations=3)

paintBucket= circuit_img.copy()

cv.floodFill(paintBucket, None, seedPoint=(0,0), newVal=(255,255,255))

paintBucket = 255-paintBucket

circuit_img = paintBucket + circuit_img


#detect connected components from paintbucket and draw big rectangles over them in circuit image
# to be acurate rectangle dim = detected dimension + 2* edge -rect thickness (~ 30/2 pixel)  


num_labels, labels, stats, centroids = cv.connectedComponentsWithStats(paintBucket)

for i in range (1, num_labels) : 

    x = stats[i, cv2.CC_STAT_LEFT] - 15
    y = stats[i, cv2.CC_STAT_TOP] - 15
    w = stats[i, cv2.CC_STAT_WIDTH] + 30
    h = stats[i, cv2.CC_STAT_HEIGHT] + 30

  # drawing rectangles over gates 
    cv.rectangle (circuit_original_img , (x,y) , (x+w,y+h)
                                          ,  (125,0,255) , thickness =2) 
  

# dilate paint bucket and subtract from original image 

custom_kernel2 = np.array([[1,1,1,0,0],
                           [1,1,1,1,0],
                           [1,1,1,1,1],
                           [1,1,1,1,0],
                           [1,1,1,0,0]] ,np.uint8 )



#wires should ve the wires only

#wires = total binary image && ~( dilated paintbucket)
wires= circuit_img.copy()
wires = cv.bitwise_and(cv.bitwise_not(
                            cv.dilate(paintBucket.copy(),custom_kernel2, iterations=10) ), 
                            wires )

# some dots appear from previous op - > errosion

wires = cv2.erode(wires, (5, 5) , iterations=7)

# detecting wires



num_labels, labels, stats, centroids = cv.connectedComponentsWithStats(wires)

print(num_labels)
for i in range (1, num_labels) : 

    x = stats[i, cv2.CC_STAT_LEFT] - 15
    y = stats[i, cv2.CC_STAT_TOP] - 15
    w = stats[i, cv2.CC_STAT_WIDTH] + 30
    h = stats[i, cv2.CC_STAT_HEIGHT] + 30

  # drawing rectangles over gates 
  #should add condition to reject wires beneath certain area (noise)
    cv.rectangle (circuit_original_img , (x,y) , (x+w,y+h)
                                          ,  (25,250,125) , thickness =2) 
  

#cv2.imshow("Count", and_img)
cv.imshow("Circuit", circuit_img)
cv.imshow("wires", wires)
cv.imshow("filling", paintBucket)
cv.imshow("gatesdetection", circuit_original_img)
cv.waitKey(0)
cv.destroyAllWindows()
