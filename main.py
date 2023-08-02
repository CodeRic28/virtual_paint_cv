import cv2
import numpy as np


frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 10)

myColors = [
    [0,92,132,25,255,255], # Orange
    [98,51,0,125,208,255], # Dark Blue
    # [98,65,24,112,245,170], # Blue
    ]
myColorValues = [
    [51,153,255],
    [255,153,51]
]

def findColor(img, myColors,myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        result = cv2.bitwise_and(img, img, mask=mask)
        # cv2.imshow(str(color[0]),result)
        x,y = getContours(mask)
        cv2.circle(imgResult,(x,y),10,myColorValues[count],cv2.FILLED)
        count+=1

def getContours(img):
    x,y,w,h = -1,-1,-1,-1
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>500:
            # cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 4)
            peri = cv2.arcLength(cnt,True)
            #Find corner points of each of the shape
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            # Bounding box
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2,y

while True:
    success, img = cap.read()
    imgResult = img.copy()
    findColor(img, myColors,myColorValues)
    cv2.imshow("Result", imgResult)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

