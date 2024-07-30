import cv2
import numpy as np
import json
from API_multiball import call_api
pixels_per_cm_x = 640 / 5  # for width
pixels_per_cm_y = 480 / 5  # for height

def white_ball_detect(url,headers):
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.resize(frame, (640, 480))
        blured_frame = cv2.GaussianBlur(frame, (5, 5), 0)  # using blurred frame to avoid noise 
        hsv_frame = cv2.cvtColor(blured_frame, cv2.COLOR_BGR2HSV)  # using HSV frame for color accuracy (white)
         
        lower_white = np.array([0, 0, 168])
        upper_white = np.array([172, 111, 255])
        white_mask = cv2.inRange(hsv_frame, lower_white, upper_white)
        
        kernel = np.ones((5, 5), np.uint8)
        white_mask = cv2.erode(white_mask, kernel, iterations=2)  # removing small white objects (noise)
        white_mask = cv2.dilate(white_mask, kernel, iterations=2)  # restoring original size of objects
        
        contours, _ = cv2.findContours(white_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        boundary_size_cm = 5
        boundary_size_pixels_x = boundary_size_cm * pixels_per_cm_x
        boundary_size_pixels_y = boundary_size_cm * pixels_per_cm_y
        
        top_left_x = (640 - boundary_size_pixels_x) // 2
        top_left_y = (480 - boundary_size_pixels_y) // 2
        bottom_right_x = top_left_x + boundary_size_pixels_x
        bottom_right_y = top_left_y + boundary_size_pixels_y
        
        cv2.rectangle(frame, (int(top_left_x), int(top_left_y)),
                      (int(bottom_right_x), int(bottom_right_y)), (255, 255, 0), 2)
        
        response_text = ""  # Initialize response text
        ball_id = 1  # Start with the first ball ID
        
        for contour in contours:
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            
            if perimeter != 0:
                circulatory = 4 * np.pi * (area / (perimeter * perimeter))
            else:
                circulatory = 0
                
            if 1900 < area < 5000 and 0.8 <= circulatory <= 1.2:
                x, y, w, h = cv2.boundingRect(contour)
                
                center_x_pixels = x + w // 2
                center_y_pixels = y + h // 2
                
                # Convert pixels to centimeters
                center_x_cm = center_x_pixels / pixels_per_cm_x
                center_y_cm = center_y_pixels / pixels_per_cm_y
                
                # Draw bounding box, contours, and center point
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.drawContours(frame, [contour], -1, (0, 255, 0), 1)
                cv2.circle(frame, (center_x_pixels, center_y_pixels), 5, (255, 255, 0), -1)
                
                # Show distance of ball from the boundary
                cv2.putText(frame, f"Ball_id {ball_id} center({center_x_cm:.2f},{center_y_cm:.2f}) cm ",
                            (center_x_pixels - 50, center_y_pixels - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
                
                dist_x = min(abs(center_x_pixels - top_left_x), abs(center_x_pixels - bottom_right_x))
                dist_y = min(abs(center_y_pixels - top_left_y), abs(center_y_pixels - bottom_right_y))
                
                # Convert distance to cm
                dist_x_cm = dist_x / pixels_per_cm_x
                dist_y_cm = dist_y / pixels_per_cm_y
                
                # Show the distance off center of ball from the boundary
                cv2.putText(frame, f"Ball_id {ball_id} Dist to boundary : X={dist_x_cm:.2f}, Y={dist_y_cm:.2f} cm ",
                            (10, 30 + ball_id * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
                
                # Make distance line from boundary to the ball center
                cv2.line(frame, (center_x_pixels, center_y_pixels), (int(center_x_pixels), 0), (0, 255, 255), 2)
                cv2.line(frame, (center_x_pixels, center_y_pixels), (0, int(center_y_pixels)), (0, 255, 255), 2)
                
                # Send ball coordinates to the API
                response = call_api(url, ball_id,center_x_cm, center_y_cm, headers)
                
                if response:
                    print(f"API Response Status Code: {response.status_code}")
                    try:
                        response_json = response.json()
                        response_text += f"Ball {ball_id}: " + ", ".join([f"{key}: {value}" for key, value in response_json.items()]) + "\n"
                        print(f"API Response JSON: {response_json}")
                    except ValueError:
                        response_text += f"Ball {ball_id}: Response content is not in JSON format\n"
                        print(response_text)
                
                ball_id += 1  # Increment ball ID
        
        # Display the API responses in the bottom right corner
        y0, dy = frame.shape[0] - 50, 15  # Adjust y0 to move the text lower
        for i, line in enumerate(response_text.split('\n')):
            y = y0 + i * dy
            cv2.putText(frame, line, (frame.shape[1] - 300, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        
        cv2.imshow("white ball detected", frame)
        
        if cv2.waitKey(1) & 0xFF == ord("c"):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    url = ""
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    white_ball_detect(url,headers)
