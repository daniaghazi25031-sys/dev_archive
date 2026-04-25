import cv2
import numpy as np
import random


width, height = 640, 480
score = 0
apple_pos = [random.randint(50, 600), 0]
apple_speed = 10

cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)


lower_color = np.array([35, 100, 100]) 
upper_color = np.array([85, 255, 255])

while True:
    success, img = cap.read()
    if not success: break
    img = cv2.flip(img, 1)
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_color, upper_color)
    
   
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        
        largest_contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest_contour) > 500:
            M = cv2.moments(largest_contour)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
           
            cv2.circle(img, (cx, cy), 20, (255, 0, 0), 3)
            
            
            distance = ((cx - apple_pos[0])**2 + (cy - apple_pos[1])**2)**0.5
            if distance < 50:
                score += 1
                apple_pos = [random.randint(50, 600), 0]

   
    apple_pos[1] += apple_speed
    if apple_pos[1] > height:
        apple_pos = [random.randint(50, 600), 0]
        score = max(0, score - 1)

    cv2.circle(img, (apple_pos[0], apple_pos[1]), 25, (0, 0, 255), cv2.FILLED)
    cv2.putText(img, f'Score: {score}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

    cv2.imshow("Color Tracking Game (No MediaPipe)", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()