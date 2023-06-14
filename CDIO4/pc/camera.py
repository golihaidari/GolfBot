import cv2
import numpy as np
from roboflow import Roboflow


def detectBalls(frame):
    # Load the Roboflow model for ball detection
    rf = Roboflow(api_key="cMW2MDLBCvueMKT3Gbfj")
    project = rf.workspace().project("golfbot-2")
    model = project.version(5).model

    ballPositionList= []
 
    while True:
        # Use the model to detect the balls
        detections = model.predict(np.asarray(frame), confidence=40, overlap= 30)

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
    rf = Roboflow(api_key="s11nf9RUEgQq22fDC5xh")
    project = rf.workspace().project("robotdetection-lfmog")
    model = project.version(2).model

    robotPosition= (0,0)
    while True:
        # Use the model to detect the robots
        detections = model.predict(np.asarray(frame), confidence=40, overlap= 30)

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

 
def detectWall(frame): 
    rf = Roboflow(api_key="cMW2MDLBCvueMKT3Gbfj")
    project = rf.workspace().project("golfbot-2")
    model = project.version(5).model

    wallPosition= (0,0)
    while True:
        # Use the model to detect the wall
        detections = model.predict(np.asarray(frame), confidence=40, overlap= 30)

        # Get the position of the center of each wall
        for detection in detections:
            if detection["class"] == "Wall":
                x = int(detection["x"])
                y = int(detection["y"])
                print("Wall position: ({}, {})".format(x, y))
                # Draw a circle around the detected wall
                cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)
                wallPosition= (x,y)
        break
    return wallPosition
    


def detectGoal(frame):
    # Acessing the roboflow model
    rf = Roboflow(api_key="cMW2MDLBCvueMKT3Gbfj")
    project = rf.workspace().project("golfbot-2")
    model = project.version(5).model

    # List is used to detect the two goals
    goalPositionList = []

    while True:
        # Detecting goals using the roboflow model
        detections = model.predict(np.asarray(frame), confidence=40, overlap= 30)

        # Get the position of the center of each goal
        for detection in detections:
            if detection["class"] == "Goal":
                x = int(detection["x"])
                y = int(detection["y"])
                print("Goal position: ({}, {})".format(x, y))
                # Draw a yellow circle around the detected goals
                cv2.circle(frame, (x, y), 10, (0, 255, 255), -1)
                goalPositionList.append((x,y))
        break
    return goalPositionList
    

def detectObstacle(frame): 
    rf = Roboflow(api_key="cMW2MDLBCvueMKT3Gbfj")
    project = rf.workspace().project("golfbot-2")
    model = project.version(5).model

    obstaclePosition= (0,0)
    while True:
        # Use the model to detect the obstacle
        detections = model.predict(np.asarray(frame), confidence=40, overlap= 30)

        # Get the position of the center of each obstacle
        for detection in detections:
            if detection["class"] == "Obstacle":
                x = int(detection["x"])
                y = int(detection["y"])
                print("Obstacle position: ({}, {})".format(x, y))
                # Draw a circle around the detected obstacle
                cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)
                obstaclePosition= (x,y)
        break
    return obstaclePosition