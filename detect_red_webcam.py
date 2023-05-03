import cv2
import numpy as np

def captureRed():

   # Create a VideoCapture object
   cam = cv2.VideoCapture(0)
   
   # Check if camera opened successfully
   if not cam.isOpened():
       print("Could not open camera")
   
   else:
       # Read frame from camera
       ret, frame = cam.read()
   
       # Check if frame is valid
       if not ret:
           print("Could not read frame")
   
       else:
           # Convert frame from RGB to HSV
           hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
   
           # Define the lower and upper bounds of the lower red range
           lower_red1 = np.array([0, 50, 50])
           upper_red1 = np.array([10, 255, 255])

           # Define the lower and upper bounds of the upper red range
           lower_red2 = np.array([170, 50, 50])
           upper_red2 = np.array([180, 255, 255])
   
           # Create masks for the red ranges
           mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
           mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
   
           # Combine the masks
           mask = mask1 + mask2
   
           # Apply the mask to the original image
           result = cv2.bitwise_and(frame, frame, mask=mask)
   
           # Display the frame in a window
           cv2.imshow("Webcam Photo", frame)
   
           # Wait for key press
           key = cv2.waitKey(0)
   
           # Press 'r' key to retake photo
           if key == ord('r'):
              captureRed()
   
           # Press 's' key to save photo
           if key == ord('s'):
               # save the result as an image file
               cv2.imwrite("webcam_photo_red.png", result)
               print("Photo saved as webcam_photo_red.png")
   
           # Destroy displayed window
           cv2.destroyWindow("Webcam Photo")
           
   # Release camera
   cam.release()

# Calling functions
captureRed()