import cv2
import numpy as np

cap=cv2.VideoCapture(0)
    
while True:
    ret, frame=cap.read()
    if not ret :
        break
    blured_frame=cv2.GaussianBlur(frame,(5,5),0)
    hsv_frame=cv2.cvtColor(blured_frame,cv2.COLOR_BGR2HSV)
    
    lower_white=np.array([0,0,168])
    upper_white=np.array([172,111,255])
    white_mask=cv2.inRange(hsv_frame,lower_white,upper_white)
    
    kernel=np.ones((5,5),np.uint8)
    white_mask=cv2.erode(white_mask,kernel,iterations=2)
    white_mask=cv2.dilate(white_mask,kernel,iterations=2)
    
    contours, _ =cv2.findContours(white_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    ball_detected=False
    ball_bbox=None
    
    for contour in contours:
        area=cv2.contourArea(contour)
        
        perimeter=cv2.arcLength(contour,True)
        
        if perimeter != 0:
            circulatory=4 * np.pi * (area/(perimeter*perimeter))
            
        else:
            circulatory=0
            
        if area > 500 and 0.7 <= circulatory <= 1.2:
            x,y,w,h = cv2.boundingRect(contour)
            
            ball_bbox=(x,y,w,h )
            ball_detected=True
            
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3)
            cv2.drawContours(frame,[contour],-1,(0,255,0),2)
            
            
        if not ball_detected:
            if ball_bbox is not None:
                ball_bbox=(x,y,w,h)
                
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            
        cv2.imshow("white ball detected",frame)
        
    if cv2.waitKey(1) & 0xFF==ord("c"):
        break
    

cap.release()
cv2.destroyAllWindows()