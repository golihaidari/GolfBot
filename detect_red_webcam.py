import cv2 as cv
import numpy as np

# Used for webcam
cap = cv.VideoCapture(0)

# Error check for webcam
if (cap.isOpened()== False): 
  print("Error opening video stream or file")

# Continue filming until q is pressed
while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:

    # Converting from RGB to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_RGB2HSV)

    # Define the lower and upper bounds of color red in HSV values
    # lower bounds (0-10)
    lower_red1 = np.array([0, 50, 50])
    upper_red1 = np.array([10, 255, 255])

    # upper bounds (170-180)
    lower_red2 = np.array([170, 50, 50])
    upper_red2 = np.array([180, 255, 255])

    # Creating two masks for the lower and upper bound and combining them
    mask1 = cv.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv.inRange(hsv, lower_red2, upper_red2)
    finalMask = mask1 + mask2

    # Obtaining masked frame
    filtered = cv.bitwise_and(frame, frame, mask=finalMask)

    # Display the original and filtered frames at the same time
    cv.imshow('Original',frame)
    cv.imshow('Filtered',filtered)

    # Exit webcam mode by pressing q
    if cv.waitKey(25) & 0xFF == ord('q'):
      break

  # Breaks the loop
  else: 
    break

# Release the video capture object
cap.release()

# Destroy all windows
cv.destroyAllWindows()