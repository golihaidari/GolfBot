import cv2
import numpy as np
from roboflow import Roboflow

# Load the Roboflow model for robot detection
rf = Roboflow(api_key="ESRzWPjCiZtf8PN9Dtmv")
project = rf.workspace().project("golfbot-pil31")
model = project.version(1).model

# Define the range of red color for field detection
red_lower = np.array([0, 0, 150])
red_upper = np.array([50, 50, 255])



def detect_robot(frame): 
    

    while True:
        # Convert the frame to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Apply the red color range to extract the field
        mask = cv2.inRange(hsv, red_lower, red_upper)
        field = cv2.bitwise_and(frame, frame, mask=mask)

        # Use the model to detect the robot
        detections = model.predict(np.asarray(frame))

        # Get the position of the center of each robot
        for detection in detections:
            if detection["class"] == "Robot":
                x = int(detection["x"])
                y = int(detection["y"])
                print("Robot position: ({}, {})".format(x, y))


