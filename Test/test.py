import cv2
import numpy as np
from roboflow import Roboflow

from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.hubs import EV3Brick

# Load the Roboflow model for ball and wall detection
rf = Roboflow(api_key="smPgmTT9SfHLAuUcQiQc")
project = rf.workspace().project("golfbot-ltfwe")
model = project.version(3).model

# Define the range of red color for field detection
red_lower = np.array([0, 0, 150])
red_upper = np.array([50, 50, 255])

# Initialize the motors.
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

# Function to control the robot based on ball coordinates
def control_robot(x, threshold_value):
    if x < threshold_value:
        # Move the robot to the left
        left_motor.run(500)
        right_motor.run(200)
    elif x > threshold_value:
        # Move the robot to the right
        left_motor.run(200)
        right_motor.run(500)
    else:
        # Stop the robot (ball is in the desired position)
        left_motor.stop()
        right_motor.stop()

def main():
    # Open the video stream
    cap = cv2.VideoCapture(1)

    # Camera parameters
    fov = 60  # Field of view in degrees
    distance = 160  # Distance between the camera and the field in centimeters
    field_width = 180  # Field width in centimeters

    # Calculate pixels per centimeter
    image_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    pixels_per_cm = image_width / field_width

    # Calculate threshold value
    threshold_value = pixels_per_cm * 100

    while True:
        # Read a frame from the video stream
        ret, frame = cap.read()

        # Convert the frame to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Apply the red color range to extract the field
        mask = cv2.inRange(hsv, red_lower, red_upper)
        field = cv2.bitwise_and(frame, frame, mask=mask)

        # Use the model to detect the balls and walls
        detections = model.predict(np.asarray(frame))

        # Get the position of the center of each ball and wall
        for detection in detections:
            x = int(detection["x"])
            y = int(detection["y"])
            label = detection["class"]

            # Draw a circle or line based on the detected class
            if label == "tableTennisBalls":
                # Draw a circle around the detected ball
                cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)
            elif label == "walls":
                # Draw a line where the wall is detected
                cv2.line(frame, (x, 0), (x, frame.shape[0]), (0, 0, 255), 2)

            # Control the robot based on ball coordinates
            if label == "tableTennisBalls":
                control_robot(x, threshold_value)

        # Display the image with the detected balls, walls, and field
        cv2.imshow("Frame", frame)
        cv2.imshow("Field", field)
        key = cv2.waitKey
