import cv2

def find_camera_index(max_index=10):
    for index in range(max_index):
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                # Display the frame to confirm it's the correct camera
                cv2.imshow(f'Camera {index}', frame)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                cap.release()
                return index
            cap.release()
    return -1  # Return -1 if no camera is found

external_camera_index = find_camera_index()
if external_camera_index != -1:
    print(f'External camera found at index: {external_camera_index}')
else:
    print('No external camera found.')
