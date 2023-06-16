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
                ballPositionList.append((x,y))
                print("Ball position: ({}, {})".format(x, y))
        break
    return ballPositionList


def detectRobot(frame):
    rf = Roboflow(api_key="s11nf9RUEgQq22fDC5xh")
    project = rf.workspace().project("robotdetection-lfmog")
    model = project.version(2).model

    robotPosition= (0,0,0)
    # Use the model to detect the robots
    detections = model.predict(np.asarray(frame), confidence=40, overlap= 30)
    # Get the position of the center of each robot
    for detection in detections:
        if detection["class"] == "robot":
            x = int(detection["x"])
            y = int(detection["y"])
            width = int(detection["width"])              
            if (x > 0) or (y > 0):
                robotPosition= (x,y,width)
                print("Robot position: ({}, {}, {})".format(x, y, width))
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
                wallPosition.append((x,y))
                print("Wall position: ({}, {})".format(x, y))
        break
    return wallPosition
    


def detectGates(frame): 
    rf = Roboflow(api_key="cMW2MDLBCvueMKT3Gbfj")
    project = rf.workspace().project("golfbot-2")
    model = project.version(5).model

    gatePosition= (0,0)
    while True:
        # Use the model to detect the gate
        detections = model.predict(np.asarray(frame), confidence=40, overlap= 30)

        # Get the position of the center of each gate
        for detection in detections:
            if detection["class"] == "Goal":
                x = int(detection["x"])
                y = int(detection["y"])                
                gatePosition.append((x,y))
                print("Gate position: ({}, {})".format(x, y))
        break
    return gatePosition
    

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
                obstaclePosition= (x,y)
                print("Obstacle position: ({}, {})".format(x, y))
        break
    return obstaclePosition