# Sources:
# # Color scheme conversion tutorial
# # Image thresholding tutorial
# # Bounding box contour tutorial

import cv2 as cv
import numpy as np
cap = cv.VideoCapture(0)
while(1):
    # Take each frame
    _, frame = cap.read()
    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # define range of color in HSV
    lower = np.array([110,50,50])
    #upper = np.array([100,170,170])
    upper = np.array([130,255,255])
    # Threshold the HSV image
    mask = cv.inRange(hsv, lower, upper)
    # Bitwise-AND mask and original image
    res = cv.bitwise_and(frame,frame, mask= mask)
    # Convert to grayscale and threshold such that object is white
    gray = cv.cvtColor(res, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(gray,50,255,cv.THRESH_BINARY)
    # Find contours of white regions
    contours, hierarchy = cv.findContours(thresh,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    # Search through all contours and draw largest corresponding rectangle
    max_area = 0
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        i,j,k,l = cv.boundingRect(cnt)
        if k*l > max_area:
            x,y,w,h = i,j,k,l
            max_area = k*l
    
    cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),thickness=4)
    cv.imshow('frame',frame)
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break
cv.destroyAllWindows()
