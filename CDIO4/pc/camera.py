from roboflow import Roboflow
import cv2
import numpy as np
from ultralytics import YOLO
from ultralytics.yolo.utils.plotting import Annotator

# Load the model from the local .pt file
model = YOLO('best.pt')

def detectBalls(frame):
    ballPositionList = []
    results = model.predict(frame)

    # Get the position of the center of each ball
    for r in results:
        boxes = r.boxes
        for box in boxes:
            b = box.xyxy[0]  # get box coordinates in (top, left, bottom, right) format
            c = box.cls
            conf = box.conf.item()
            if model.names[int(c)] == "tableTennisBalls":
                x = int((b[2] + b[0]) / 2)
                y = int((b[3] + b[1]) / 2)
                print(f"Ball position: ({x}, {y})")
                # Draw a circle around the detected ball
                cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)
                ballPositionList.append((x, y))

    return ballPositionList

'''
def detectRobot(frame):
    rf = Roboflow(api_key="cMW2MDLBCvueMKT3Gbfj")
    project = rf.workspace().project("robotdetection-jvv38")
    model = project.version(1).model

    robotPosition = (0, 0)
    while True:
        # Use the model to detect the robots
        detections = model.predict(np.asarray(frame), confidence=20, overlap=5)

        # Get the position of the center of each robot
        for detection in detections:
            if detection["class"] == "robot":
                x = int(detection["x"])
                y = int(detection["y"])
                print("Robot position: ({}, {})".format(x, y))
                # Draw a circle around the detected robot
                cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)
                robotPosition = (x, y)
        break
    return robotPosition
'''

# need implementation!!!
def detect_wall(frame):
    return (0, 0)


# Open a connection to the webcam
cap = cv2.VideoCapture(0)

while True:
    # Capture a frame from the webcam
    ret, frame = cap.read()

    ballPositionList = detectBalls(frame)

    cv2.imshow('Camera Feed', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam when done
cap.release()

cv2.destroyAllWindows()
