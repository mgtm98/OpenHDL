import cv2
import numpy as np

cv = cv2

circuit_img = cv2.imread('./Images/test.jpg', 0)
and_img = cv2.imread('./Images/and.jpg', 0)

circuit_img = cv2.resize(
    circuit_img, (circuit_img.shape[1]//2, circuit_img.shape[0]//2))
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

cv2.floodFill(paintBucket, None, seedPoint=(0,0), newVal=(255,255,255))

circuit_img = 255- paintBucket + circuit_img



#circuit_img = cv.Canny(circuit_img , 240 , 255 )




#cv2.imshow("Count", and_img)
cv2.imshow("Circuit", circuit_img)
cv2.imshow("filling", 255-paintBucket)
cv2.waitKey(0)
cv.destroyAllWindows()
