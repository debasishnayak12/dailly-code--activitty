import cv2
face_cap=cv2.CascadeClassifier("C:/Users/madhu/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0/LocalCache/local-packages/Python311/site-packages/cv2/data/haarcascade_frontalface_alt2.xml")
video_cap=cv2.VideoCapture(0)

while True:
    ret,video_data=video_cap.read()
    col=cv2.cvtColor(video_data,cv2.COLOR_BGR2GRAY)
    objects=face_cap.detectMultiScale(
        col,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30,30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    
    for (x,y,w,h) in objects:
        cv2.rectangle(video_data,(x,y),(x+w,y+h),(255,0,0),3)
        
        cv2.imshow("Face_derector",video_data)
        if cv2.waitKey(1) & 0xFF == ord("c"):
            break
        
    video_cap.release()
    cv2.destroyAllWindows()