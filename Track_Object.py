import cv2
import numpy as np
print(cv2.__version__)

dispW = 640
dispH = 480
#flip = 2
#camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3464, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'


####################################################################
def nothing(x):
    pass

cv2.namedWindow('Trackbars')
cv2.moveWindow('Trackbars',1600,0)

cv2.createTrackbar('hueLow','Trackbars',50,179,nothing)
cv2.createTrackbar('hueHigh','Trackbars',100,179,nothing)

cv2.createTrackbar('hue2Low','Trackbars',50,179,nothing)
cv2.createTrackbar('hue2High','Trackbars',100,179,nothing)

cv2.createTrackbar('satLow','Trackbars',100,255,nothing)
cv2.createTrackbar('satHigh','Trackbars',255,255,nothing)
cv2.createTrackbar('valLow','Trackbars',100,255,nothing)
cv2.createTrackbar('valHigh','Trackbars',255,255,nothing)



cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,dispW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,dispH)

while(True):
    ret, frame = cam.read()

    #frame = cv2.imread('smarties.png')
    #cv2.imshow('logitech', frame)
    #cv2.moveWindow('logitech',0,0)

    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    hueLow = cv2.getTrackbarPos('hueLow','Trackbars')
    hueHigh = cv2.getTrackbarPos('hueHigh','Trackbars')

    hue2Low = cv2.getTrackbarPos('hue2Low','Trackbars')
    hue2High = cv2.getTrackbarPos('hue2High','Trackbars')

    satLow = cv2.getTrackbarPos('satLow','Trackbars')
    satHigh = cv2.getTrackbarPos('satHigh','Trackbars')

    valLow = cv2.getTrackbarPos('valLow','Trackbars')
    valHigh = cv2.getTrackbarPos('valHigh','Trackbars')

    lowerBound = np.array([hueLow, satLow, valLow])
    upperBound = np.array([hueHigh, satHigh, valHigh])

    lowerBound2 = np.array([hue2Low, satLow, valLow])
    upperBound2 = np.array([hue2High, satHigh, valHigh])

    FGMask = cv2.inRange(hsv,lowerBound,upperBound)
    FGMask2 = cv2.inRange(hsv,lowerBound2,upperBound2)
    FGmaskComp = cv2.add(FGMask,FGMask2)
    cv2.imshow('FGMaskComp', FGmaskComp)
    cv2.moveWindow('FGMaskComp',0,520)

    contours,_ = cv2.findContours(FGmaskComp,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours,key=lambda x:cv2.contourArea(x),reverse=True)
    
    for cnt in contours:

        area = cv2.contourArea(cnt)
        (x,y,w,h) = cv2.boundingRect(cnt)
        if area >= 50 :
            #cv2.drawContours(frame,[cnt],0,(255,0,0),2)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

    #cv2.drawContours(frame,contours,0,(255,0,0),2)

    cv2.imshow('logitech', frame)
    cv2.moveWindow('logitech',0,0)


    #FG = cv2.bitwise_and(frame,frame,mask=FGmaskComp)
    #cv2.imshow('FG', FG)
    #cv2.moveWindow('FG',500,0)

    #BGMask = cv2.bitwise_not(FGmaskComp)
    #cv2.imshow('BG Mask', BGMask)
    #cv2.moveWindow('BG Mask',500,520)

    #BG = cv2.cvtColor(BGMask,cv2.COLOR_GRAY2BGR)

    #final = cv2.add(BG,FG)
    #cv2.imshow('Final', final)
    #cv2.moveWindow('Final',1000,0)


    if cv2.waitKey(1)==ord('q'):
        break

cam.release()
cv2.destroyAllWindows()