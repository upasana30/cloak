#import libraries
import numpy as np
import cv2
import time

cap = cv2.VideoCapture("D:\upasana\projects\python\invisible cloak.mp4")#camera is not started yeh it is just to initalize the camera

time.sleep(2)

background = 0

#caputring the background
for i in range(30):
    ret, background = cap.read()#for capturing background
    
while(cap.isOpened()):
    ret, img = cap.read()#for capturing operation on it
    
    if not ret:
        break
        
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #HSB
    #saturation is basically the darkness we take it here 120 b'coz if is below this value the it would go towards the red, white, or pink color
    #value is basically the brightness of the color if brightness is below 70 is whould hampper it
    #HSV values
    lower_red = np.array([0 , 120, 70])
    upper_red = np.array([10 , 255, 255])
    
    mask1 = cv2.inRange(hsv , lower_red, upper_red)#seperating the cloak part
    
    lower_red = np.array([170 , 120, 70])
    upper_red = np.array([180 , 255, 255])
    
    mask2 = cv2.inRange(hsv, lower_red, upper_red)
    
    mask1 = mask1+mask2#we are using add operatior for bitwise OR
    
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))
    #basically morphopen removes all the noise
    #mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3,3), np.uint8), iteration=1)
    #to increase smoothness of the image 
    
    mask2 = cv2.bitwise_not(mask1)#except the cloak everthing would be there
    
    res1 = cv2.bitwise_and(background, background, mask=mask1)#used for segmentation of the color
    res2 = cv2.bitwise_and(img, img, mask=mask2)#used to substitue the cloak part
    
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)#addweighted is use to lineraly add two images
    
    cv2.imshow('output', final_output)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()