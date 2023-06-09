import cv2
import numpy as np
from roboflow import Roboflow


def detectBalls(frame):
    # Load the Roboflow model for ball detection
    rf = Roboflow(api_key="smPgmTT9SfHLAuUcQiQc")
    project = rf.workspace().project("golfbot-ltfwe")
    model = project.version(3).model

    ballPositionList= []
 
    while True:
        # Use the model to detect the balls
        detections = model.predict(np.asarray(frame))

        # Get the position of the center of each ball
        for detection in detections:
            if detection["class"] == "tableTennisBalls":
                x = int(detection["x"])
                y = int(detection["y"])
                print("Ball position: ({}, {})".format(x, y))
                # Draw a circle around the detected ball
                cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)
                ballPositionList.append((x,y))
        break
    return ballPositionList


def detectRobot(frame):
    rf = Roboflow(api_key="cMW2MDLBCvueMKT3Gbfj")
    project = rf.workspace().project("robotdetection-jvv38")
    model = project.version(1).model

    robotPosition= (0,0)
    while True:
        # Use the model to detect the robots
        detections = model.predict(np.asarray(frame), confidence=20, overlap= 5)

        # Get the position of the center of each robot
        for detection in detections:
            if detection["class"] == "robot":
                x = int(detection["x"])
                y = int(detection["y"])
                print("Robot position: ({}, {})".format(x, y))
                # Draw a circle around the detected robot
                cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)
                robotPosition= (x,y)
        break
    return robotPosition

 
def detect_wall(frame): 
    rf = Roboflow(api_key="cMW2MDLBCvueMKT3Gbfj")
    project = rf.workspace().project("robotdetection-jvv38")
    model = project.version(1).model

    wallPosition= (0,0)
    while True:
        # Use the model to detect the wall
        detections = model.predict(np.asarray(frame), confidence=20, overlap= 5)

        # Get the position of the center of each wall
        for detection in detections:
            if detection["class"] == "wall":
                x = int(detection["x"])
                y = int(detection["y"])
                print("Wall position: ({}, {})".format(x, y))
                # Draw a circle around the detected wall
                cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)
                wallPosition= (x,y)
        break
    return wallPosition
    


def detectGate(frame): 
    rf = Roboflow(api_key="cMW2MDLBCvueMKT3Gbfj")
    project = rf.workspace().project("robotdetection-jvv38")
    model = project.version(1).model

    gatePosition= (0,0)
    while True:
        # Use the model to detect the gate
        detections = model.predict(np.asarray(frame), confidence=20, overlap= 5)

        # Get the position of the center of each gate
        for detection in detections:
            if detection["class"] == "gate":
                x = int(detection["x"])
                y = int(detection["y"])
                print("Gate position: ({}, {})".format(x, y))
                # Draw a circle around the detected gate
                cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)
                gatePosition= (x,y)
        break
    return gatePosition
    

def detectObstacle(frame): 
    rf = Roboflow(api_key="cMW2MDLBCvueMKT3Gbfj")
    project = rf.workspace().project("robotdetection-jvv38")
    model = project.version(1).model

    obstaclePosition= (0,0)
    while True:
        # Use the model to detect the obstacle
        detections = model.predict(np.asarray(frame), confidence=20, overlap= 5)

        # Get the position of the center of each obstacle
        for detection in detections:
            if detection["class"] == "obstacle":
                x = int(detection["x"])
                y = int(detection["y"])
                print("Obstacle position: ({}, {})".format(x, y))
                # Draw a circle around the detected obstacle
                cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)
                obstaclePosition= (x,y)
        break
    return obstaclePosition
